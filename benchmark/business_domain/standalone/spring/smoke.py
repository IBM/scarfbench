#!/usr/bin/env python3
"""Smoke test for Jakarta EE standalone application on Spring Boot.

Checks:
  1) GET <base>/greet returns 200 and `Greetings!` message.

Exit codes:
  0 success, non-zero on first failure encountered.
"""

import os
import sys
import time
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

GREET_PATH = "/greet"
VERBOSE = os.getenv("VERBOSE") == "1"
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080/standalone")


def vprint(msg: str):
    if VERBOSE:
        print(msg)


def http_request(
    method: str,
    url: str,
    data: bytes | None = None,
    headers: dict | None = None,
    timeout: int = 10,
):
    req = Request(url, data=data, method=method, headers=headers or {})
    try:
        with urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8", "replace")
    except HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8", "replace")
    except (URLError, Exception) as e:  # network failure
        return None, f"NETWORK-ERROR: {e}"
    return (status, body), None


def assert_greet(base: str):
    url = base.rstrip("/") + GREET_PATH
    resp, err = http_request("GET", url)
    if err:
        print(f"[FAIL] Greet check error: {err}", file=sys.stderr)
        sys.exit(1)
    status, body = resp
    if status != 200:
        print(f"[FAIL] Greet check status: {status}", file=sys.stderr)
        sys.exit(1)
    try:
        greet_data = json.loads(body)
        if greet_data.get("message") != "Greetings!":
            print(f"[FAIL] Greet message missmatch: {body}", file=sys.stderr)
            sys.exit(1)
    except json.JSONDecodeError:
        print(f"[FAIL] Greet check invalid JSON: {body}", file=sys.stderr)
        sys.exit(1)
    print("[PASS] GET greet")


def main():
    start = time.time()

    assert_greet(BASE_URL)

    elapsed = time.time() - start
    print(f"[PASS] Smoke sequence complete in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
