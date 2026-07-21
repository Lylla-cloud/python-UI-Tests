import base64
from typing import List, Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver: WebDriver, timeout_seconds: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout_seconds)

    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def wait_for_element_visible(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator: tuple) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple) -> None:
        element = self.wait_for_element_clickable(locator)
        self.highlight_element(element)
        element.click()

    def type(self, locator: tuple, text: str) -> None:
        element = self.wait_for_element_visible(locator)
        self.highlight_element(element)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.wait_for_element_visible(locator).text

    def is_element_present(self, locator: tuple) -> bool:
        return len(self.driver.find_elements(*locator)) > 0

    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def highlight_element(self, element: WebElement) -> None:
        try:
            self.execute_script("arguments[0].style.border='3px solid red'; arguments[0].style.backgroundColor='yellow';", element)
        except Exception:
            pass

    def capture_screenshot_base64(self) -> Optional[str]:
        try:
            return self.driver.get_screenshot_as_base64()
        except Exception:
            return None

    def get_all_href_links(self) -> List[str]:
        links = []
        anchors = self.driver.find_elements(By.TAG_NAME, "a")
        for anchor in anchors:
            try:
                href = anchor.get_attribute("href")
                if href and href.strip() and not href.startswith("javascript:") and not href.startswith("#"):
                    links.append(href.strip())
            except Exception:
                pass
        return links
