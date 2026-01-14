#!/usr/bin/env python3
"""Smoke test for billpayment-spring

Checks:
  1) Visit and validate contents of Base Page
  2) Pay using the Debit card option
  3) Go back to main page
  4) Pay using the Credit card option
  5) Go back to main page
  6) Reset payment form

Exit codes:
  0 success
  1 failure
"""

import os
import sys
from datetime import datetime
from playwright.sync_api import Page, sync_playwright


DEFAULT_BASE = "http://localhost:8080"
BASE_URL = os.getenv("BILLPAYMENT_BASE_URL", DEFAULT_BASE)
DEFAULT_ENDPOINT = "/"
HOME_URI = os.getenv("BILLPAYMENT_HOME_URI", DEFAULT_ENDPOINT)


def visit_main_page(page: Page) -> int:
    passed = 0
    page.goto(BASE_URL + HOME_URI)
    # Ensure that the page loads successfully
    if "Bill Payment Options" in page.content():
        print("[PASS] Page loaded successfully and contains expected text.")
        passed = 1
    else:
        print("[FAIL] Page did not contain expected text.", file=sys.stderr)

    return passed


def pay(page: Page, amount: int, card_type: str) -> int:
    passed = 0

    # Fill the amount input and pay
    page.get_by_label("Amount: $").fill(f"{amount}")
    page.get_by_label(f"{card_type} Card").check()
    with page.expect_navigation():
        page.get_by_role("button", name="Pay").click()

    # Assert we're on result page
    page_content = page.content().lower()
    if all(
        elem.lower() in page_content
        for elem in ["Bill Payment: Result", card_type.upper(), f"{amount}.00"]
    ):
        print(f"[PASS] {card_type} payment displayed correctly.")
        passed = 1
    else:
        print(f"[FAIL] {card_type} payment not displayed as expected.", file=sys.stderr)

    return passed


def back(page: Page) -> int:
    passed = 0
    # Hit the back button and ensure we are back on the form
    with page.expect_navigation():
        page.get_by_role("button", name="Back").click()
    if "Bill Payment Options" in page.content():
        print("[PASS] Back navigation successful.")
        passed = 1
    else:
        print("[FAIL] Back navigation failed.", file=sys.stderr)

    return passed


def reset(page: Page) -> int:
    passed = 0
    page.get_by_label("Amount: $").fill("12")
    with page.expect_navigation():
        page.get_by_role("button", name="Reset").click()

    if "0" == page.get_by_label("Amount: $").input_value():
        print("[PASS] Reset successful.")
        passed = 1
    else:
        print("[FAIL] Reset failed.", file=sys.stderr)

    return passed


def main() -> int:
    print(f"---[ {datetime.now().strftime('%H:%M:%S')} - Smoke test ]---")
    with sync_playwright() as p:
        num_tests = 0
        passed_tests = 0
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        num_tests += 1
        passed_tests += visit_main_page(page)

        num_tests += 1
        # Fill the amount input and pay with debit card
        passed_tests += pay(page=page, amount=12, card_type="Debit")

        num_tests += 1
        # Hit the back button and ensure we are back on the form
        passed_tests += back(page)

        num_tests += 1
        # Fill the amount input and pay with credit card
        passed_tests += pay(page=page, amount=5, card_type="Credit")

        num_tests += 1
        # Hit the back button and ensure we are back on the form
        passed_tests += back(page)

        num_tests += 1
        # Click the "Reset" button
        passed_tests += reset(page)

        print(f"Summary: {passed_tests}/{num_tests} tests passed.")
        print(f"---[ {datetime.now().strftime('%H:%M:%S')} - Smoke test complete ]---")
        return 0 if num_tests == passed_tests else 1


if __name__ == "__main__":
    sys.exit(main())
