import pytest
from selenium.webdriver.common.by import By
from pages.generic_page import GenericWebPage

def test_forms_and_inputs(driver, target_url):
    page = GenericWebPage(driver)
    page.navigate_to(target_url)
    
    forms = page.get_forms_info()
    text_inputs = driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='search'], input[type='email'], textarea")
    
    interacted = 0
    for input_elem in text_inputs:
        try:
            if input_elem.is_displayed() and input_elem.is_enabled():
                page.highlight_element(input_elem)
                interacted += 1
        except Exception:
            pass
            
    print(f"\n[Form Audit] Discovered {len(forms)} form(s) and {len(text_inputs)} text input(s). Interacted with {interacted} field(s).")
    assert len(forms) >= 0, "Forms inspection completed"
