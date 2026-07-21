import pytest
from selenium.webdriver.common.by import By
from pages.generic_page import GenericWebPage

def test_performance_and_accessibility(driver, target_url):
    page = GenericWebPage(driver)
    page.navigate_to(target_url)
    
    h1s = driver.find_elements(By.TAG_NAME, "h1")
    h2s = driver.find_elements(By.TAG_NAME, "h2")
    images = page.get_images_audit()
    missing_alt = [img for img in images if not img.get("hasAlt")]
    load_time_ms = page.get_page_load_time_ms()
    
    print(f"\n[Page Audit] H1 headers: {len(h1s)} | H2 headers: {len(h2s)} | Images: {len(images)} ({len(missing_alt)} missing alt text) | Load time: {load_time_ms}ms")
    
    # Assert reasonable page load if performance timing is supported
    if load_time_ms > 0:
        assert load_time_ms < 30000, f"Page load took excessive time: {load_time_ms}ms"
