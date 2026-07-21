import pytest
from pages.generic_page import GenericWebPage

def test_site_availability_and_smoke(driver, target_url):
    page = GenericWebPage(driver)
    page.navigate_to(target_url)
    
    current_url = page.get_current_url()
    title = page.get_title()
    meta_tags = page.get_meta_tags()
    screenshot = page.capture_screenshot_base64()
    
    assert current_url.startswith("http"), f"Unexpected URL protocol: {current_url}"
    assert title and len(title.strip()) > 0, "Page title is missing or empty!"
    assert screenshot is not None, "Failed to capture page screenshot"
    
    print(f"\n[Smoke Test] Target: {target_url} | Loaded URL: {current_url} | Title: '{title}' | Meta tags: {len(meta_tags)}")
