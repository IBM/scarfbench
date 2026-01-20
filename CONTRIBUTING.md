# Contributing to SCARFBench

This guide explains how to contribute a new application to the SCARFBench benchmark suite.

## Table of Contents

- [Overview](#overview)
- [Required Files](#required-files)
- [1. Dockerfile](#1-dockerfile)
- [2. Justfile](#2-justfile)
- [3. Smoke Test (smoke.py)](#3-smoke-test-smokepy)
- [Standard Patterns](#standard-patterns)
- [Checklist](#checklist)

## Overview

Each benchmark application in SCARFBench should support three frameworks:
- **Jakarta EE** (using Open Liberty)
- **Quarkus**
- **Spring Boot**

In addition to the source application files, each framework implementation requires three standard files:
1. `Dockerfile` - Container definition
2. `justfile` - Build and run automation
3. `smoke.py` - Automated smoke tests

This guide uses the [`benchmark/infrastructure/concurrency-jobs`](benchmark/infrastructure/concurrency-jobs) application as the reference standard.

## Required Files

### 1. Dockerfile

The Dockerfile creates a containerized environment for building and running your application.

#### Standard Structure (Basic Pattern)

For applications with simple REST/HTTP API testing:

```dockerfile
FROM eclipse-temurin:21-jdk

USER root
RUN apt-get update && apt-get install -y python3 curl && rm -rf /var/lib/apt/lists/*
RUN useradd -m -u 1001 <framework-user>

USER <framework-user>
WORKDIR /app

# Copy all project files
COPY --chown=1001:1001 pom.xml .
COPY --chown=1001:1001 .mvn .mvn
COPY --chown=1001:1001 mvnw .
COPY --chown=1001:1001 src src
COPY --chown=1001:1001 smoke.py .

RUN chmod +x mvnw

# Default command matches your local workflow
CMD ["./mvnw", "clean", "package", "<framework-specific-goal>"]
```

#### Playwright Pattern (For UI/Browser Testing)

For applications requiring browser automation and UI testing (reference: [`benchmark/infrastructure/ejb-async`](benchmark/infrastructure/ejb-async)):

```dockerfile
FROM eclipse-temurin:17-jdk

# Run everything as root (needed for Playwright installation)
USER root

# Install Python and needed tools (add python3-venv for virtual environment support)
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip curl && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment for Python dependencies (PEP 668 safe)
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Shared browsers path so Chromium is cached once
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN mkdir -p /ms-playwright && chmod 755 /ms-playwright

# Install Playwright and Chromium dependencies inside venv
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && pip install --no-cache-dir playwright==1.47.0 \
 && playwright install --with-deps chromium

WORKDIR /app

# Copy Maven wrapper first (cache efficient)
COPY .mvn .mvn
COPY mvnw .
RUN chmod +x mvnw

# Copy root pom and module poms for dependency layer caching
COPY pom.xml ./
# If you have multiple modules, copy each module's pom separately:
# COPY module1/pom.xml module1/pom.xml
# COPY module2/pom.xml module2/pom.xml
RUN ./mvnw -q -DskipTests dependency:go-offline || true

# Copy full module sources
COPY src src
# If you have multiple modules:
# COPY module1 module1
# COPY module2 module2

# Copy unified smoke test (includes Playwright logic)
COPY smoke.py .
RUN chmod +x smoke.py

# For Playwright tests, CMD can run smoke.py directly or the Maven goal
CMD ["./mvnw", "clean", "package", "<framework-specific-goal>"]
# Or for smoke-test-only images:
# CMD ["python3", "smoke.py"]
```

#### Important Notes

1. **Python3 and curl**: Always install these for smoke tests
2. **User ID 1001**: Standard non-root user for security (basic pattern only)
3. **Root User for Playwright**: Playwright installation requires root privileges; use root user when browser automation is needed
4. **Virtual Environment**: Use Python venv (`/opt/venv`) for Playwright to comply with PEP 668
5. **File Ownership**: Use `--chown=1001:1001` for all COPY commands in basic pattern; omit in Playwright pattern (root owns everything)
6. **smoke.py**: Must be copied into the container
7. **No Port Exposure**: Do NOT use `EXPOSE` directive - tests run internally via `docker exec`, not through exposed ports
8. **Maven Wrapper**: Ensure `mvnw` is executable with `chmod +x`
9. **Layer Caching**: For Playwright pattern, copy pom.xml files first to cache dependencies separately from source code
10. **Browser Path**: Set `PLAYWRIGHT_BROWSERS_PATH=/ms-playwright` to share browser binaries across builds

### 2. Justfile

The justfile provides standard commands for building, running, testing, and managing your application.

#### Standard Structure

```just
### <Application Name> (<Framework>) Justfile
APP_NAME       := "<app-name>-<framework>"
IMAGE_NAME     := "<app-name>-<framework>:latest"

build:
	docker build -f Dockerfile -t {{IMAGE_NAME}} .
	@echo "[INFO] Built image: {{IMAGE_NAME}}"

rebuild:
	docker build --no-cache -f Dockerfile -t {{IMAGE_NAME}} .
	@echo "[INFO] Rebuilt image (no cache): {{IMAGE_NAME}}"

up: build
    ### The below section will look for exisiting containers and if so, remove them. 
	@if docker ps --all --quiet --filter name=^/{{APP_NAME}}$ | grep -q .; then \
		echo "[INFO] Removing existing container"; \
		docker rm -f {{APP_NAME}} >/dev/null; \
	fi
    
    ### Run the container in detached mode
	docker run -d --name {{APP_NAME}} {{IMAGE_NAME}}
	@echo "[INFO] Started {{APP_NAME}}, waiting for app to start..."

    ### Look for framework-specific startup pattern in logs and wait until found (see below for patterns)
	@until docker logs {{APP_NAME}} 2>&1 | grep -q "<startup-pattern>"; do sleep 1; done
	@echo "[INFO] App started and ready."

logs:
	docker logs -f {{APP_NAME}}

down:
	- docker rm -f {{APP_NAME}}
	@echo "[INFO] Container removed (if it existed)"

test: up
    @docker exec {{APP_NAME}} sh -c 'python3 /app/smoke.py'

local:
	./mvnw clean package <framework-goal>
```

#### Framework-Specific Startup Patterns

The `up` target waits for the application to start by monitoring container logs for specific patterns:

| Framework | Startup Pattern |
|-----------|-----------------|
| Jakarta | `CWWKF0011I` |
| Quarkus | `"loggerName":"io.quarkus".*started in .*Listening on:` |
| Spring Boot | `Tomcat started on port <PORT>\|Started .* in .* seconds` |

#### Port Notes

Applications bind to internal ports (usually `9080` or `8080`) for communication within the container. Since tests run internally via `docker exec`, **no port mapping to the host is needed**. The justfile does not expose ports, and containers run without `-p` flags.

#### Required Targets

All justfiles must include these standard targets:

- `build`: Build the Docker image
- `rebuild`: Rebuild without cache (for troubleshooting)
- `up`: Start container, wait for readiness
- `logs`: Stream container logs
- `down`: Stop and remove container
- `test`: Run smoke tests
- `local`: Run locally without Docker

### 3. Smoke Test (smoke.py)

The smoke test is a Python script that validates your application's core functionality.

#### Standard Structure

```python
#!/usr/bin/env python3
"""Smoke test for <Application Name> (<Framework>).

Checks:
  1) Discover reachable base path
  2) <Test 1 description>
  3) <Test 2 description>
  ...

Exit codes:
  0 success, non-zero on first failure encountered.
"""
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Configuration
VERBOSE = os.getenv("VERBOSE") == "1"

# Base URL candidates (try in order)
CANDIDATES = [
    os.getenv("<APP>_BASE_URL"),  # Environment variable override
    "http://localhost:<internal-port>/<path>/",  # Container internal
]

def vprint(msg: str):
    """Print only if VERBOSE=1"""
    if VERBOSE:
        print(msg)

def http_request(
    method: str,
    url: str,
    data: bytes | None = None,
    headers: dict | None = None,
    timeout: int = 10,
):
    """Make HTTP request, return (status, body) or None on network error"""
    req = Request(url, data=data, method=method, headers=headers or {})
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8", "replace")
    except HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8", "replace")
    except (URLError, Exception) as e:
        return None, f"NETWORK-ERROR: {e}"
    return (status, body), None

def discover_base() -> str:
    """Try each candidate URL, return first working one"""
    for cand in CANDIDATES:
        if not cand:
            continue
        # Try to validate candidate
        if validate_candidate(cand):
            print(f"[INFO] Base discovered: {cand}")
            return cand
    # Fallback
    for cand in CANDIDATES:
        if cand:
            print(f"[WARN] No base validated, using fallback {cand}")
            return cand
    print("[ERROR] No base URL candidates available", file=sys.stderr)
    sys.exit(2)

def validate_candidate(base: str) -> bool:
    """Implement validation logic for your app"""
    # Example: Try a health check endpoint
    pass

def main():
    start = time.time()
    base = discover_base()
    
    # Run your test sequence here
    # Example:
    # test_endpoint_1(base)
    # test_endpoint_2(base)
    
    elapsed = time.time() - start
    print(f"[PASS] Smoke sequence complete in {elapsed:.2f}s")
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

#### Key Components

1. **Docstring**: Describe what the smoke test validates
2. **URL Discovery**: Try multiple URL candidates (env var, localhost variations, container ports)
3. **HTTP Helper**: Reusable function for making requests
4. **Verbose Logging**: Support `VERBOSE=1` environment variable
5. **Exit Codes**: Use specific exit codes for different failure types
6. **Pass/Fail Messages**: Clear `[PASS]`/`[FAIL]` prefixes
7. **Timing**: Report total test execution time

#### Playwright-Based Testing (Advanced)

For applications requiring browser automation and UI testing, use Playwright. Example structure:

```python
#!/usr/bin/env python3
"""Smoke test with Playwright for UI validation.

Checks:
  1) Start application server
  2) Launch browser and navigate to UI
  3) Interact with UI elements
  4) Validate UI behavior and responses

Exit codes:
  0 success, non-zero on failure.
"""
import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

VERBOSE = os.getenv("VERBOSE") == "1"
BASE_URL = "http://localhost:9080"

def vprint(msg: str):
    if VERBOSE:
        print(msg)

def start_server():
    """Start the application server"""
    vprint("[INFO] Starting application server...")
    # Example: Start Liberty server
    proc = subprocess.Popen(
        ["./mvnw", "clean", "package", "liberty:run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for server to be ready
    for line in proc.stdout:
        vprint(line.rstrip())
        if "CWWKF0011I" in line:  # Liberty started
            print("[INFO] Server started successfully")
            break
    
    return proc

def test_ui_with_playwright(base_url: str):
    """Test UI using Playwright browser automation"""
    print("[INFO] Launching browser...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to application
            vprint(f"[INFO] Navigating to {base_url}")
            page.goto(base_url, wait_until="networkidle", timeout=30000)
            
            # Example: Check page title
            title = page.title()
            if "Expected Title" not in title:
                print(f"[FAIL] Unexpected page title: {title}", file=sys.stderr)
                return False
            print(f"[PASS] Page title: {title}")
            
            # Example: Fill form and submit
            page.fill("#inputField", "test value")
            page.click("#submitButton")
            
            # Wait for response
            page.wait_for_selector(".result", timeout=10000)
            result = page.text_content(".result")
            
            if "expected result" not in result.lower():
                print(f"[FAIL] Unexpected result: {result}", file=sys.stderr)
                return False
            print(f"[PASS] Form submission successful: {result}")
            
            return True
            
        except PlaywrightTimeout as e:
            print(f"[FAIL] Timeout: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"[FAIL] Error: {e}", file=sys.stderr)
            return False
        finally:
            browser.close()

def main():
    start = time.time()
    
    # Start server
    server_proc = start_server()
    
    try:
        # Run UI tests
        success = test_ui_with_playwright(BASE_URL)
        
        if not success:
            return 1
        
        elapsed = time.time() - start
        print(f"[PASS] Smoke sequence complete in {elapsed:.2f}s")
        return 0
        
    finally:
        # Clean up
        if server_proc:
            vprint("[INFO] Stopping server...")
            server_proc.terminate()
            server_proc.wait()

if __name__ == "__main__":
    sys.exit(main())
```

#### Playwright Testing Notes

1. **Browser Setup**: Use `chromium.launch(headless=True)` for CI/CD compatibility
2. **Timeouts**: Set appropriate timeouts for page loads and element waits
3. **Wait Strategies**: Use `wait_until="networkidle"` for page loads, `wait_for_selector` for elements
4. **Error Handling**: Always use try/finally to ensure browser cleanup
5. **Server Management**: Start application server before tests, terminate after
6. **Selectors**: Use stable selectors (IDs, data attributes) instead of classes
7. **Screenshots**: Capture on failure for debugging: `page.screenshot(path="error.png")`
8. **Virtual Display**: In Docker, browsers run headless automatically

#### Best Practices

1. **Test Real Functionality**: Don't just check if the server responds - validate actual behavior
2. **Multiple Scenarios**: Test with and without authentication, different inputs, etc.
3. **Meaningful Assertions**: Check status codes AND response content
4. **Clear Error Messages**: Include URL, status, and response body in failures
5. **Early Exit**: Exit on first failure with specific exit code
6. **Timeout Handling**: Use reasonable timeouts (10s default)
7. **Network Resilience**: Handle both HTTP errors and network failures

#### Example Test Pattern

```python
def test_endpoint(base: str, description: str, path: str, 
                  method: str = "GET", expected_status: int = 200,
                  expected_content: str = None, headers: dict = None):
    """Reusable test function"""
    url = f"{base.rstrip('/')}{path}"
    resp, err = http_request(method, url, headers=headers)
    
    if err:
        print(f"[FAIL] {description}: {err}", file=sys.stderr)
        sys.exit(1)
    
    status, body = resp
    body_stripped = body.strip()
    
    if status != expected_status:
        print(f"[FAIL] {description}: Expected {expected_status}, got {status}", 
              file=sys.stderr)
        sys.exit(1)
    
    if expected_content and expected_content not in body_stripped:
        print(f"[FAIL] {description}: Expected content '{expected_content}' not found",
              file=sys.stderr)
        sys.exit(1)
    
    print(f"[PASS] {description}")
```

## Standard Patterns

### Directory Structure

```
benchmark/<category>/<application-name>/
├── jakarta/
│   ├── Dockerfile
│   ├── justfile
│   ├── smoke.py
│   ├── pom.xml
│   ├── mvnw
│   ├── mvnw.cmd
│   ├── .mvn/
│   └── src/
├── quarkus/
│   ├── Dockerfile
│   ├── justfile
│   ├── smoke.py
│   ├── pom.xml
│   ├── mvnw
│   ├── mvnw.cmd
│   ├── .mvn/
│   └── src/
└── spring/
    ├── Dockerfile
    ├── justfile
    ├── smoke.py
    ├── pom.xml
    ├── mvnw
    ├── mvnw.cmd
    ├── .mvn/
    └── src/
```

### Naming Conventions

1. **Container Names**: `<app>-<framework>` (e.g., `jobs-jakarta`, `jobs-quarkus`)
2. **Image Names**: `<app>-<framework>:latest`
3. **Variables**: Use uppercase with underscores (e.g., `APP_NAME`, `IMAGE_NAME`)
4. **Paths**: Use consistent endpoint paths across frameworks

### Common Variables

These should appear in every justfile:

```just
APP_NAME       := "<app>-<framework>"
IMAGE_NAME     := "<app>-<framework>:latest"
```

## Checklist

Before submitting your contribution, verify:

### Dockerfile
- [ ] Uses appropriate JDK base image for framework
- [ ] Installs `python3` and `curl`
- [ ] **Basic pattern**: Creates non-root user with UID 1001
- [ ] **Playwright pattern**: Runs as root and installs Python venv, pip, and Playwright
- [ ] **Playwright pattern**: Sets up `PLAYWRIGHT_BROWSERS_PATH` and installs Chromium
- [ ] Copies all necessary files with correct ownership (use `--chown=1001:1001` for basic pattern)
- [ ] Makes `mvnw` executable
- [ ] Does NOT include `EXPOSE` directive (tests run internally)
- [ ] Uses correct Maven goal in CMD
- [ ] **Playwright pattern**: Implements layer caching for pom.xml files

### Justfile
- [ ] All variables defined at top (APP_NAME, IMAGE_NAME)
- [ ] `build` target works
- [ ] `rebuild` target works (no cache)
- [ ] `up` target waits for correct startup pattern
- [ ] `logs` target streams container logs
- [ ] `down` target cleans up container
- [ ] `test` target runs smoke tests successfully
- [ ] `local` target runs app without Docker

### Smoke Test (smoke.py)
- [ ] Has descriptive docstring
- [ ] Includes shebang `#!/usr/bin/env python3`
- [ ] Has URL discovery with multiple candidates
- [ ] Supports `VERBOSE=1` environment variable
- [ ] Tests real application functionality (not just health checks)
- [ ] Uses clear `[PASS]`/`[FAIL]` messages
- [ ] Exits with code 0 on success, non-zero on failure
- [ ] Reports execution time
- [ ] Handles network errors gracefully
- [ ] Works both inside container and from host
- [ ] **Playwright tests**: Properly manages browser lifecycle (launch/close)
- [ ] **Playwright tests**: Uses appropriate timeouts and wait strategies
- [ ] **Playwright tests**: Handles server startup and shutdown

### Testing
- [ ] `just build` succeeds for all frameworks
- [ ] `just up` starts container and waits for ready state
- [ ] `just test` passes all smoke tests
- [ ] `just logs` shows application logs
- [ ] `just down` cleans up successfully
- [ ] `just local` runs application locally
- [ ] All three frameworks (jakarta, quarkus, spring) work identically
- [ ] **Playwright tests**: Browser tests pass in headless mode
- [ ] **Playwright tests**: Tests work both inside container and from host

### Documentation
- [ ] Add README.md explaining the application's purpose
- [ ] Document any special configuration or requirements
- [ ] Document if Playwright is used for UI testing
- [ ] Update main benchmark documentation if needed

## Tips and Troubleshooting

### Dockerfile Tips
- Use multi-stage builds if you need to reduce image size
- Clear apt cache with `rm -rf /var/lib/apt/lists/*` to reduce layer size
- Pin Java versions if your app requires specific version
- **Playwright**: Always use Python venv to comply with PEP 668
- **Playwright**: Set `PLAYWRIGHT_BROWSERS_PATH` to cache browsers efficiently
- **Playwright**: Copy pom.xml files first for better layer caching

### Justfile Tips
- Test startup patterns with: `docker logs <container> 2>&1 | grep -q "<pattern>"`
- Use `-d` flag for `docker run` to run in background
- The `-` prefix in `down` target suppresses errors if container doesn't exist

### Smoke Test Tips
- Run with `VERBOSE=1 python3 smoke.py` for debugging
- Test from inside container: `docker exec <container> python3 /app/smoke.py`
- Use `curl` within container to manually test endpoints before automating
- **Playwright**: Use `headless=False` locally for visual debugging
- **Playwright**: Capture screenshots on failure: `page.screenshot(path="error.png")`
- **Playwright**: Use `page.pause()` to debug interactively during development

### Common Issues

**Container won't start**: Check logs with `docker logs <container>`

**Smoke test fails**: Run with `VERBOSE=1` to see detailed request/response

**Startup timeout**: Increase sleep or check startup pattern regex

**Permission denied**: Verify file ownership matches user UID 1001 (basic pattern only)

**Playwright browser won't launch**: Ensure you're running as root in Dockerfile or install system dependencies

**Playwright timeout**: Increase timeout values or check if page is actually loading

**Python package conflicts**: Use virtual environment with `python3 -m venv` (required for Playwright)

**Chromium not found**: Verify `playwright install chromium` ran successfully and `PLAYWRIGHT_BROWSERS_PATH` is set

## Example Workflow

1. Create framework directories (jakarta, quarkus, spring)
2. Implement application in each framework
3. **Decide on testing approach**: Basic (REST/HTTP) or Playwright (UI/Browser)
4. Write Dockerfile for first framework (use appropriate pattern)
5. Write justfile with unique port
6. Test with `just build && just up`
7. Write smoke.py to validate functionality
8. Test with `just test`
9. Copy and adapt Dockerfile/justfile/smoke.py to other frameworks
10. Adjust framework-specific settings (base image, startup pattern, goals, ports)
11. Verify all frameworks work: `just test` in each directory
12. Document in README.md

## Getting Help

- Check existing benchmarks in `benchmark/` for examples
- **Basic pattern reference**: [`benchmark/infrastructure/concurrency-jobs`](benchmark/infrastructure/concurrency-jobs)
- **Playwright pattern reference**: [`benchmark/infrastructure/ejb-async`](benchmark/infrastructure/ejb-async)
- Open an issue if you have questions

---

Thank you for contributing to SCARFBench!
