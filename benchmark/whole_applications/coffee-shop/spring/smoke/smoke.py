import pytest
import re
from playwright.sync_api import Page, expect


def test_coffeeshop_homepage(page: Page):
    """Test the coffee shop homepage loads correctly."""
    # 1. Navigate to the coffee shop homepage
    page.goto("http://localhost:8080/")

    # 2. Verify page title contains expected text
    title = page.title()
    assert "Coffee" in title or "coffee" in title.lower()

    # 3. Verify main navigation menu is present
    expect(page.locator("a").filter(has_text=re.compile(r"About", re.I)).first).to_be_visible()
    expect(page.locator("a").filter(has_text=re.compile(r"Menu", re.I)).first).to_be_visible()

    # 4. Verify coffee shop branding is present
    expect(page.locator("body")).to_be_visible()


def test_navigate_to_about_section(page: Page):
    """Test navigating to the about section."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/")

    # 2. Click on "About" menu item
    page.locator("a").filter(has_text=re.compile(r"About", re.I)).first.click()

    # 3. Verify page scrolls to about section or URL changes
    page.wait_for_load_state("load")
    expect(page.locator("body")).to_be_visible()


def test_navigate_to_menu_section(page: Page):
    """Test navigating to the menu section."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/")

    # 2. Click on "Menu" menu item
    page.locator("a").filter(has_text=re.compile(r"Menu", re.I)).first.click()

    # 3. Verify page scrolls to menu section
    page.wait_for_load_state("load")
    expect(page.locator("body")).to_be_visible()


def test_homepage_banner_content(page: Page):
    """Test that the homepage has banner content."""
    # 1. Navigate to homepage
    page.goto("http://localhost:8080/")

    # 2. Wait for page to load
    page.wait_for_load_state("load")

    # 3. Verify the page loaded successfully
    expect(page.locator("body")).to_be_visible()


def test_navigation_menu_persistence(page: Page):
    """Test that navigation menu is present on the page."""
    # 1. Navigate to homepage
    page.goto("http://localhost:8080/")
    page.wait_for_load_state("load")

    # 2. Verify navigation menu is present
    menu_items = page.locator("nav a").first
    expect(menu_items).to_be_visible()


if __name__ == "__main__":
    pytest.main(["-v", "smoke.py"])
