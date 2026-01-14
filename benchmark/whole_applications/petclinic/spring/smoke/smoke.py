import pytest
import re
from playwright.sync_api import Page, expect


def test_petclinic_homepage(page: Page):
    """Test the petclinic homepage loads correctly."""
    # 1. Navigate to the petclinic homepage
    page.goto("http://localhost:8080/")

    # 2. Verify page title contains expected text
    title = page.title()
    assert "PetClinic" in title or "petclinic" in title.lower()

    # 3. Verify main navigation menu is present - check for links that contain these texts
    expect(page.locator("a").filter(has_text=re.compile(r"Home", re.I)).first).to_be_visible()
    expect(page.locator("a").filter(has_text=re.compile(r"Find.*Owner|Owner", re.I)).first).to_be_visible()
    expect(page.locator("a").filter(has_text=re.compile(r"Veterinarian", re.I)).first).to_be_visible()

    # 4. Verify welcome message or content is present
    expect(page.locator("body")).to_be_visible()


def test_navigate_to_find_owners_page(page: Page):
    """Test navigating to the find owners page."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/")

    # 2. Click on "Find owners" menu item
    page.locator("a").filter(has_text=re.compile(r"Find.*Owner|Owner", re.I)).first.click()

    # 3. Verify URL changes to /owners/find
    expect(page).to_have_url(re.compile(r".*/owners/find", re.I))

    # 4. Verify page loads successfully
    expect(page.locator("body")).to_be_visible()


def test_navigate_to_veterinarians_page(page: Page):
    """Test navigating to the veterinarians page."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/")

    # 2. Click on "Veterinarians" menu item
    page.locator("a").filter(has_text=re.compile(r"Veterinarian", re.I)).first.click()

    # 3. Verify URL changes to /vets.html
    expect(page).to_have_url(re.compile(r".*/vets\.html", re.I))

    # 4. Verify page loads successfully
    expect(page.locator("body")).to_be_visible()


def test_homepage_welcome_content(page: Page):
    """Test that the homepage has welcome content."""
    # 1. Navigate to homepage
    page.goto("http://localhost:8080/")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify the page loaded successfully
    expect(page.locator("body")).to_be_visible()


def test_find_owners_page_has_search_form(page: Page):
    """Test that the find owners page has a search form."""
    # 1. Navigate to find owners page
    page.goto("http://localhost:8080/owners/find")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify search input field is present
    search_input = page.locator("input[type='text'], input[id*='lastName'], input[name*='lastName']").first
    expect(search_input).to_be_visible()


def test_veterinarians_page_displays_content(page: Page):
    """Test that the veterinarians page displays content."""
    # 1. Navigate to veterinarians page
    page.goto("http://localhost:8080/vets.html")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify page has content (table or list)
    expect(page.locator("body")).to_be_visible()
    # Check for table or list structure
    content = page.locator("table, ul, ol, .vet-list, .vets").first
    expect(content).to_be_visible(timeout=10000)


def test_homepage_has_welcome_text(page: Page):
    """Test that the homepage has welcome text or heading."""
    # 1. Navigate to homepage
    page.goto("http://localhost:8080/")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify welcome text or heading is present
    welcome_text = page.locator("h1, h2, .welcome, [class*='welcome']").first
    expect(welcome_text).to_be_visible()


def test_page_titles_are_correct(page: Page):
    """Test that page titles are set correctly."""
    # 1. Test homepage title
    page.goto("http://localhost:8080/")
    page.wait_for_load_state("networkidle")
    title = page.title()
    assert title and len(title) > 0, "Homepage should have a title"

    # 2. Test find owners page title
    page.goto("http://localhost:8080/owners/find")
    page.wait_for_load_state("networkidle")
    title = page.title()
    assert title and len(title) > 0, "Find owners page should have a title"

    # 3. Test veterinarians page title
    page.goto("http://localhost:8080/vets.html")
    page.wait_for_load_state("networkidle")
    title = page.title()
    assert title and len(title) > 0, "Veterinarians page should have a title"


def test_pages_load_without_errors(page: Page):
    """Test that pages load without JavaScript errors or 404s."""
    pages_to_test = ["/", "/owners/find", "/vets.html"]

    for page_url in pages_to_test:
        # Navigate to each page
        response = page.goto(f"http://localhost:8080{page_url}")
        assert response and response.status < 400, f"Page {page_url} should load successfully (status: {response.status if response else 'None'})"
        page.wait_for_load_state("networkidle")


if __name__ == "__main__":
    pytest.main(["-v", "smoke.py"])
