#!/usr/bin/env python3
"""Smoke test for Jakarta EE cart application on Quarkus.

Checks:
  1) Discover reachable cart API base path.
  2) GET <base>/health returns 200 and status=UP.
  3) POST <base>/initialize creates a cart session.
  4) POST <base>/books/{title} adds books to cart.
  5) GET <base>/books returns books list with correct count.
  6) DELETE <base>/books/{title} removes a book.
  7) DELETE <base> clears the cart.

Exit codes:
  0 success, non-zero on first failure encountered.
"""

import os
import sys
import time
import json
from urllib.request import Request, build_opener, HTTPCookieProcessor
from urllib.error import HTTPError, URLError
import http.cookiejar as cookiejar

HEALTH_PATH = "/health"
INITIALIZE_PATH = "/initialize"
BOOKS_PATH = "/books"
API_HEADER = "Content-Type"
VERBOSE = os.getenv("VERBOSE") == "1"

CANDIDATES = [
    os.getenv("CART_BASE_URL"),
    "http://localhost:9080/cart/api/cart",
    "http://localhost:8080/cart/api/cart",
]

COOKIE_JAR = cookiejar.CookieJar()
HTTP = build_opener(HTTPCookieProcessor(COOKIE_JAR))


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
        with HTTP.open(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8", "replace")
    except HTTPError as e:
        status = e.code
        body = e.read().decode("utf-8", "replace")
    except (URLError, Exception) as e:  # network failure
        return None, f"NETWORK-ERROR: {e}"
    return (status, body), None


def try_health_check(base: str):
    url = base.rstrip("/") + HEALTH_PATH
    vprint(f"Attempt GET {url}")
    resp, err = http_request("GET", url)
    if err:
        vprint(f"Fail: {err}")
        return False
    status, body = resp
    if status != 200:
        vprint(f"Unexpected status {status}")
        return False
    try:
        health_data = json.loads(body)
        if health_data.get("status") == "UP":
            return True
    except json.JSONDecodeError:
        vprint(f"Health check response not valid JSON: {body}")
    return False


def discover_base() -> str:
    for cand in CANDIDATES:
        if not cand:
            continue
        if try_health_check(cand):
            print(f"[INFO] Base discovered: {cand}")
            return cand
    # fallback to first non-empty candidate even if no health check
    for cand in CANDIDATES:
        if cand:
            print(f"[WARN] No base validated, using fallback {cand}")
            return cand
    print("[ERROR] No base URL candidates available", file=sys.stderr)
    sys.exit(2)


def assert_health(base: str):
    url = base.rstrip("/") + HEALTH_PATH
    resp, err = http_request("GET", url)
    if err:
        print(f"[FAIL] Health check error: {err}", file=sys.stderr)
        sys.exit(3)
    status, body = resp
    if status != 200:
        print(f"[FAIL] Health check status: {status}", file=sys.stderr)
        sys.exit(3)
    try:
        health_data = json.loads(body)
        if health_data.get("status") != "UP":
            print(f"[FAIL] Health status not UP: {body}", file=sys.stderr)
            sys.exit(3)
    except json.JSONDecodeError:
        print(f"[FAIL] Health check invalid JSON: {body}", file=sys.stderr)
        sys.exit(3)
    print("[PASS] GET health -> status=UP")


def initialize_cart(base: str, customer_name: str, customer_id: str):
    url = base.rstrip("/") + INITIALIZE_PATH
    payload = json.dumps(
        {"customerName": customer_name, "customerId": customer_id}
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    resp, err = http_request("POST", url, data=payload, headers=headers)
    if err:
        print(f"[FAIL] Initialize cart error: {err}", file=sys.stderr)
        sys.exit(4)
    status, body = resp
    if status != 200:
        print(f"[FAIL] Initialize cart status: {status} :: {body}", file=sys.stderr)
        sys.exit(4)
    try:
        result = json.loads(body)
        if "message" not in result:
            print(
                f"[FAIL] Initialize response missing message: {body}", file=sys.stderr
            )
            sys.exit(4)
    except json.JSONDecodeError:
        print(f"[FAIL] Initialize response invalid JSON: {body}", file=sys.stderr)
        sys.exit(4)
    print(f"[PASS] POST initialize cart for '{customer_name}' -> {status}")


def add_book(base: str, title: str):
    # URL encode the title
    encoded_title = title.replace(" ", "%20")
    url = f"{base.rstrip('/')}{BOOKS_PATH}/{encoded_title}"
    headers = {"Content-Type": "application/json"}

    resp, err = http_request("POST", url, data=b"", headers=headers)
    if err:
        print(f"[FAIL] Add book '{title}' error: {err}", file=sys.stderr)
        sys.exit(5)
    status, body = resp
    if status != 200:
        print(f"[FAIL] Add book '{title}' status: {status} :: {body}", file=sys.stderr)
        sys.exit(5)
    try:
        result = json.loads(body)
        if result.get("title") != title:
            print(f"[FAIL] Add book title mismatch: {body}", file=sys.stderr)
            sys.exit(5)
    except json.JSONDecodeError:
        print(f"[FAIL] Add book response invalid JSON: {body}", file=sys.stderr)
        sys.exit(5)
    print(f"[PASS] POST add book '{title}' -> {status}")


def get_books(base: str, expected_count: int = None):
    url = base.rstrip("/") + BOOKS_PATH
    resp, err = http_request("GET", url)
    if err:
        print(f"[FAIL] Get books error: {err}", file=sys.stderr)
        sys.exit(6)
    status, body = resp
    if status != 200:
        print(f"[FAIL] Get books status: {status} :: {body}", file=sys.stderr)
        sys.exit(6)
    try:
        result = json.loads(body)
        books = result.get("books", [])
        count = result.get("count", 0)
        if expected_count is not None and count != expected_count:
            print(
                f"[FAIL] Expected {expected_count} books, got {count}: {books}",
                file=sys.stderr,
            )
            sys.exit(6)
        print(f"[PASS] GET books -> count={count}, books={books}")
        return books
    except json.JSONDecodeError:
        print(f"[FAIL] Get books response invalid JSON: {body}", file=sys.stderr)
        sys.exit(6)


def remove_book(base: str, title: str, should_fail: bool = False):
    # URL encode the title
    encoded_title = title.replace(" ", "%20")
    url = f"{base.rstrip('/')}{BOOKS_PATH}/{encoded_title}"

    resp, err = http_request("DELETE", url)
    if err:
        print(f"[FAIL] Remove book '{title}' error: {err}", file=sys.stderr)
        sys.exit(7)
    status, body = resp

    if should_fail:
        if status == 404:
            try:
                result = json.loads(body)
                if "error" in result:
                    print(
                        f"[PASS] DELETE book '{title}' (expected failure) -> {status}"
                    )
                    return
            except json.JSONDecodeError:
                pass
        print(
            f"[FAIL] Expected 404 for '{title}', got {status}: {body}", file=sys.stderr
        )
        sys.exit(7)
    else:
        if status != 200:
            print(
                f"[FAIL] Remove book '{title}' status: {status} :: {body}",
                file=sys.stderr,
            )
            sys.exit(7)
        try:
            result = json.loads(body)
            if result.get("title") != title:
                print(f"[FAIL] Remove book title mismatch: {body}", file=sys.stderr)
                sys.exit(7)
        except json.JSONDecodeError:
            print(f"[FAIL] Remove book response invalid JSON: {body}", file=sys.stderr)
            sys.exit(7)
        print(f"[PASS] DELETE book '{title}' -> {status}")


def clear_cart(base: str):
    url = base.rstrip("/")
    resp, err = http_request("DELETE", url)
    if err:
        print(f"[FAIL] Clear cart error: {err}", file=sys.stderr)
        sys.exit(8)
    status, body = resp
    if status != 200:
        print(f"[FAIL] Clear cart status: {status} :: {body}", file=sys.stderr)
        sys.exit(8)
    try:
        result = json.loads(body)
        if "message" not in result:
            print(
                f"[FAIL] Clear cart response missing message: {body}", file=sys.stderr
            )
            sys.exit(8)
    except json.JSONDecodeError:
        print(f"[FAIL] Clear cart response invalid JSON: {body}", file=sys.stderr)
        sys.exit(8)
    print(f"[PASS] DELETE clear cart -> {status}")


def main():
    start = time.time()

    # Discover base URL
    base = discover_base()

    # Check health
    assert_health(base)

    # Initialize cart
    initialize_cart(base, "Duke DeUrl", "123")

    # Add books
    add_book(base, "Infinite Jest")
    add_book(base, "Bel Canto")
    add_book(base, "Kafka on the Shore")

    # Get books (should be 3)
    get_books(base, expected_count=3)

    # Remove one book
    remove_book(base, "Bel Canto")

    # Get books again (should be 2)
    get_books(base, expected_count=2)

    # Try to remove non-existent book (should fail with 404)
    remove_book(base, "Gravity's Rainbow", should_fail=True)

    # Clear cart
    clear_cart(base)

    elapsed = time.time() - start
    print(f"[PASS] Smoke sequence complete in {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
