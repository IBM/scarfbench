#!/usr/bin/env python3
"""
Smoke test for Jakarta REST "Hello" app.

Checks:
  1) GET <BASE>/helloworld -> 200 and Content-Type text/html

Environment:
  HELLO_BASE   Base HTTP URL (default: http://localhost:9080/jaxrs-hello-10-SNAPSHOT)
  VERBOSE=1    Enable verbose logging

Exit codes:
  0  success
  2  GET /helloworld failed (status or content-type)
  9  Network / unexpected error
"""
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE = os.getenv("HELLO_BASE", "http://localhost:9080/jaxrs-hello-10-SNAPSHOT").rstrip("/")
VERBOSE = os.getenv("VERBOSE") == "1"
TIMEOUT = 10

def vprint(*args):
    if VERBOSE:
        print(*args)

def join(base: str, path: str) -> str:
    if not path:
        return base
    if base.endswith("/") and path.startswith("/"):
        return base[:-1] + path
    if (not base.endswith("/")) and (not path.startswith("/")):
        return base + "/" + path
    return base + path

def http(method: str, url: str, data: bytes | None = None, headers: dict | None = None):
    req = Request(url, data=data, method=method, headers=headers or {})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8", "replace")
            # Try to capture content-type (may include charset)
            content_type = resp.headers.get("Content-Type", "")
            return {"status": status, "body": body, "content_type": content_type}, None
    except HTTPError as e:
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            body = ""
        return {"status": e.code, "body": body, "content_type": e.headers.get("Content-Type", "")}, None
    except (URLError, Exception) as e:
        return None, f"NETWORK-ERROR: {e}"

def must_get_helloworld():
    url = join(BASE, "/helloworld")
    vprint(f"GET {url}")
    resp, err = http("GET", url)
    if err:
        print(f"[FAIL] GET /helloworld -> {err}", file=sys.stderr)
        sys.exit(9)
    if resp["status"] != 200:
        print(f"[FAIL] GET /helloworld -> HTTP {resp['status']}", file=sys.stderr)
        sys.exit(2)
    ctype = resp["content_type"].split(";")[0].strip().lower()
    if ctype != "text/html":
        print(f"[FAIL] GET /helloworld -> unexpected Content-Type {resp['content_type']!r}", file=sys.stderr)
        sys.exit(2)
    print("[PASS] GET /helloworld -> 200 text/html")


def main():
    print(f"[INFO] BASE = {BASE}")
    must_get_helloworld()
    print("[PASS] Smoke sequence complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
