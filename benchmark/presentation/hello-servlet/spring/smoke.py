"""
Smoke test for Hello Servlet application.

Checks:
  1) GET /greeting?name=<NAME> returns 200 and includes <NAME> in the body.
  2) GET /greeting without 'name' returns a 4xx (typically 400) with a helpful hint mentioning 'name'.

Environment:
  HELLO_BASE   Base URL, e.g. http://localhost:8080  (default: http://localhost:8080)
  SMOKE_NAME   Name to use in greeting               (default: SmokeUser)
  VERBOSE=1    Enable verbose logging

Exit codes:
  0 success; non-zero on first failure encountered:
    2  GET /greeting?name=... failed
    3  GET /greeting (missing param) did not fail as expected
    4  Network or unexpected error
"""

import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

BASE = os.getenv("HELLO_BASE", "http://localhost:8080/")
NAME = os.getenv("SMOKE_NAME", "SmokeUser")
VERBOSE = os.getenv("VERBOSE") == "1"

def vprint(*args):
    if VERBOSE:
        print(*args)

def http_request(method: str, url: str, data: bytes | None = None, headers: dict | None = None, timeout: int = 10):
    req = Request(url, data=data, method=method, headers=headers or {})
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8", "replace")
            return (status, body), None
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            body = ""
        return (e.code, body), None
    except (URLError, Exception) as e:
        return None, f"NETWORK-ERROR: {e}"

def must_get_with_name(base: str, name: str):
    url = f"{base.rstrip('/')}/greeting?{urlencode({'name': name})}"
    vprint(f"GET {url}")
    resp, err = http_request("GET", url)
    if err:
        print(f"[FAIL] {url} -> {err}", file=sys.stderr)
        sys.exit(4)
    status, body = resp
    if status != 200 or name not in body:
        print(f"[FAIL] GET {url} expected 200 and body containing {name!r}, got {status}, body={body[:200]!r}", file=sys.stderr)
        sys.exit(2)
    print(f"[PASS] GET /greeting?name=… -> 200, contains {name!r}")

def must_fail_without_name(base: str):
    url = f"{base.rstrip('/')}/greeting"
    vprint(f"GET {url} (missing 'name')")
    resp, err = http_request("GET", url)
    if err:
        print(f"[FAIL] {url} -> {err}", file=sys.stderr)
        sys.exit(4)
    status, body = resp
    if status < 400 or status >= 500:
        print(f"[FAIL] GET {url} expected 4xx, got {status}", file=sys.stderr)
        sys.exit(3)
    hint = "name" in body.lower()
    if not hint:
        print(f"[WARN] Missing 'name' hint in error body (status {status})", file=sys.stderr)
    print(f"[PASS] GET /greeting (no name) -> {status}")

def main():
    must_get_with_name(BASE, NAME)
    must_fail_without_name(BASE)
    print("[PASS] Smoke sequence complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
