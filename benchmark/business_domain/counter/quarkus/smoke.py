#!/usr/bin/env python3
"""Smoke test for counter-jakarta

Checks:
  1) Visit and validate contents of main page
  2) Visit the main page again and validate the access counter increses by 1

Exit codes:
  0 success
  1 failure
"""

import os
import re
import sys
from datetime import datetime
from playwright.sync_api import Page, sync_playwright


DEFAULT_BASE = "http://localhost:8080"
BASE_URL = os.getenv("COUNTER_BASE_URL", DEFAULT_BASE)
DEFAULT_ENDPOINT = "/counter"
HOME_URI = os.getenv("COUNTER_HOME_URI", DEFAULT_ENDPOINT)


def visit_main_page(page: Page) -> tuple[int, int]:
    passed = 0
    access_count = 0
    page.goto(BASE_URL + HOME_URI)

    # Ensure that the page loads successfully
    html = page.content()
    match = re.search(r"This page has been accessed (\d+) time\(s\)\.", html)

    if match:
        access_count = int(match.group(1))
        passed = 1

    return (passed, access_count)


def main() -> int:
    print(f"---[ {datetime.now().strftime('%H:%M:%S')} - Smoke test ]---")
    with sync_playwright() as p:
        num_tests = 0
        passed_tests = 0
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        num_tests += 1
        passed, access_counter = visit_main_page(page)
        if passed == 1:
            print("[PASS] Page loaded successfully and contains expected text.")
        else:
            print("[FAIL] Page did not contain expected text.", file=sys.stderr)
        passed_tests += passed

        # access counter should increse by 1 on each call
        num_tests += 1
        passed, next_access_counter = visit_main_page(page)
        if passed == 1 and (access_counter + 1) == next_access_counter:
            print("[PASS] Page loaded successfully and contains expected text.")
            passed_tests += passed
        else:
            print("[FAIL] Page did not contain expected text.", file=sys.stderr)

        print(f"Summary: {passed_tests}/{num_tests} tests passed.")
        print(f"---[ {datetime.now().strftime('%H:%M:%S')} - Smoke test complete ]---")
        return 0 if num_tests == passed_tests else 1


if __name__ == "__main__":
    sys.exit(main())
