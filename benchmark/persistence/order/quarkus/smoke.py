#!/usr/bin/env python3
"""
Smoke tests for order-quarkus web application.
"""
import asyncio
import aiohttp
import sys
import time
import os
from playwright.async_api import async_playwright

BASE_URL = "http://localhost:8082/"
START_TIMEOUT = int(os.getenv("START_TIMEOUT", "90"))

async def wait_for_http(host: str, port: int, timeout: int):
    url = f"http://{host}:{port}/orders"
    async with aiohttp.ClientSession() as session:
        end = time.time() + timeout
        while time.time() < end:
            try:
                async with session.get(url, timeout=5) as response:
                    print(f"[DEBUG] HTTP {response.status} from {url}")
                    if response.status == 200:
                        print(f"[DEBUG] Successfully connected to {url}")
                        return
                    else:
                        print(f"[DEBUG] Non-200 response: {response.status} from {url}")
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"[DEBUG] Waiting for {url}, error: {str(e)}")
            await asyncio.sleep(0.5)
        raise TimeoutError(f"Timed out waiting for HTTP port {port} after {timeout}s")

async def test_orders_page(page):
    await page.goto(f"{BASE_URL}orders")
    assert await page.locator("text=No orders found").count() == 0, "Expected orders to load"
    assert await page.locator("text=1111").count() > 0, "Order 1111 not found"
    assert await page.locator("text=4312").count() > 0, "Order 4312 not found"

async def test_create_order(page):
    await page.goto(f"{BASE_URL}orders")
    await page.fill('input[name="newOrderId"]', "9999")
    await page.fill('input[name="newOrderShippingInfo"]', "Test Shipping")
    await page.select_option('select[name="newOrderStatus"]', "N")
    await page.select_option('select[name="newOrderDiscount"]', "10")
    await page.click('button:has-text("Submit")')
    await page.wait_for_selector("text=9999", timeout=5000)
    assert await page.locator("text=9999").count() > 0, "New order 9999 not created"

async def test_line_items(page):
    await page.goto(f"{BASE_URL}lineItems?orderId=1111")
    assert await page.locator("text=Item ID").count() > 0, "Line items table not loaded"

async def main():
    await wait_for_http("localhost", 8082, START_TIMEOUT)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await test_orders_page(page)
            await test_create_order(page)
            await test_line_items(page)
            print("[PASS] All smoke tests passed")
            return 0
        except Exception as e:
            print(f"[FAIL] {e}", file=sys.stderr)
            return 1
        finally:
            await browser.close()

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))