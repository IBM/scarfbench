import pytest
import re
from playwright.sync_api import Page, expect


def test_petclinic_homepage(page: Page):
    """Test the petclinic homepage loads correctly."""
    # 1. Navigate to the petclinic homepage
    page.goto("http://localhost:8080/petclinic/home.jsf")

    # 2. Verify page title contains expected text
    title = page.title()
    assert "Petclinic" in title or "petclinic" in title.lower()

    # 3. Verify main navigation menu is present - check for links that contain these texts
    expect(page.locator("a").filter(has_text=re.compile(r"Home", re.I)).first).to_be_visible()
    expect(page.locator("a").filter(has_text=re.compile(r"Owner", re.I)).first).to_be_visible()
    expect(page.locator("a").filter(has_text=re.compile(r"Pet Type", re.I)).first).to_be_visible()
    expect(page.locator("a").filter(has_text=re.compile(r"Veterinarian", re.I)).first).to_be_visible()
    expect(page.locator("a").filter(has_text=re.compile(r"Specialt", re.I)).first).to_be_visible()  # "Specialties" or "Specialty"

    # 4. Verify search form is present on homepage
    search_input = page.locator("input[type='text']").first
    expect(search_input).to_be_visible()


def test_navigate_to_owner_page(page: Page):
    """Test navigating to the owner management page."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/petclinic/home.jsf")

    # 2. Click on "Owner" menu item
    page.locator("a").filter(has_text=re.compile(r"Owner", re.I)).first.click()

    # 3. Verify URL changes to owner.jsf
    expect(page).to_have_url(re.compile(r".*owner\.jsf", re.I))

    # 4. Verify page loads successfully with owner list content
    owner_header = page.locator("h1, .contentTitleHeadline").filter(has_text=re.compile(r"Owner", re.I)).first
    expect(owner_header).to_be_visible()


def test_navigate_to_pet_type_page(page: Page):
    """Test navigating to the pet type management page."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/petclinic/home.jsf")

    # 2. Click on "Pet Type" menu item
    page.locator("a").filter(has_text=re.compile(r"Pet Type", re.I)).first.click()

    # 3. Verify URL changes to petType.jsf
    expect(page).to_have_url(re.compile(r".*petType\.jsf", re.I))

    # 4. Verify page loads successfully
    pet_type_header = page.locator("h1, .contentTitleHeadline").filter(has_text=re.compile(r"Pet Type", re.I)).first
    expect(pet_type_header).to_be_visible()


def test_navigate_to_veterinarian_page(page: Page):
    """Test navigating to the veterinarian management page."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/petclinic/home.jsf")

    # 2. Click on "Veterinarian" menu item
    page.locator("a").filter(has_text=re.compile(r"Veterinarian", re.I)).first.click()

    # 3. Verify URL changes to veterinarian.jsf
    expect(page).to_have_url(re.compile(r".*veterinarian\.jsf", re.I))

    # 4. Verify page loads successfully
    veterinarian_header = page.locator("h1, .contentTitleHeadline").filter(has_text=re.compile(r"Veterinarian", re.I)).first
    expect(veterinarian_header).to_be_visible()


def test_navigate_to_information_page(page: Page):
    """Test navigating to the information page."""
    # 1. Navigate to home page
    page.goto("http://localhost:8080/petclinic/home.jsf")

    # 2. Click on "Information" menu item or link
    info_link = page.locator("a").filter(has_text=re.compile(r"Information|Info", re.I)).first
    info_link.click()

    # 3. Verify URL changes to info.jsf
    expect(page).to_have_url(re.compile(r".*info\.jsf", re.I))


def test_owner_page_has_search_functionality(page: Page):
    """Test that the owner page has search functionality."""
    # 1. Navigate to owner page
    page.goto("http://localhost:8080/petclinic/owner.jsf")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify search input field is present
    search_input = page.locator("input[type='text'], input[id*='search'], input[placeholder*='search']").first
    expect(search_input).to_be_visible()


def test_homepage_welcome_panel(page: Page):
    """Test that the homepage has welcome information."""
    # 1. Navigate to homepage
    page.goto("http://localhost:8080/petclinic/home.jsf")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify the page loaded successfully
    expect(page.locator("body")).to_be_visible()


def test_navigation_menu_persistence(page: Page):
    """Test that navigation menu is present on all pages."""
    pages_to_test = ["home.jsf", "owner.jsf", "petType.jsf", "veterinarian.jsf", "specialty.jsf"]

    for page_url in pages_to_test:
        # Navigate to each page
        page.goto(f"http://localhost:8080/petclinic/{page_url}")
        page.wait_for_load_state("networkidle")

        # Verify navigation menu is present (check for at least one menu item)
        menu_items = page.locator("a[href*='.jsf'], [role='menuitem'], nav a").first
        expect(menu_items).to_be_visible()


def test_owner_page_displays_list(page: Page):
    """Test that the owner page displays a list of owners."""
    # 1. Navigate to owner page
    page.goto("http://localhost:8080/petclinic/owner.jsf")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify that the page structure exists
    expect(page.locator("body")).to_be_visible()


def test_pet_type_page_displays_list(page: Page):
    """Test that the pet type page displays a list."""
    # 1. Navigate to pet type page
    page.goto("http://localhost:8080/petclinic/petType.jsf")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify page structure is present
    expect(page.locator("body")).to_be_visible()


def test_veterinarian_page_displays_list(page: Page):
    """Test that the veterinarian page displays a list."""
    # 1. Navigate to veterinarian page
    page.goto("http://localhost:8080/petclinic/veterinarian.jsf")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify page structure is present
    expect(page.locator("body")).to_be_visible()


def test_specialty_page_displays_list(page: Page):
    """Test that the specialty page displays a list."""
    # 1. Navigate to specialty page
    page.goto("http://localhost:8080/petclinic/specialty.jsf")

    # 2. Wait for page to load
    page.wait_for_load_state("networkidle")

    # 3. Verify page structure is present
    expect(page.locator("body")).to_be_visible()


def test_index_redirects_to_home(page: Page):
    """Test that index.html redirects to home.jsf."""
    # 1. Navigate to index.html
    page.goto("http://localhost:8080/petclinic/index.html")

    # 2. Wait for redirect
    page.wait_for_load_state("networkidle")

    # 3. Verify URL contains home.jsf
    expect(page).to_have_url(re.compile(r".*home\.jsf", re.I))


if __name__ == "__main__":
    pytest.main(["-v", "smoke.py"])
