from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_reader import ConfigReader


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, timeout=ConfigReader.get("timeout", 20))

    def find(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator))

    def click(self, locator):
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator))
            try:
                element.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            element = self.find(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def type(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def is_displayed(self, locator):
        try:
            return self.find(locator).is_displayed()
        except Exception:
            return False

    def find_all(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator))

    def scroll_to(self, locator):
        element = self.find(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", element)

    # --- Backward compatibility methods ---

    def navigate_to(self, url: str) -> None:
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    def execute_script(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def highlight_element(self, element) -> None:
        try:
            self.execute_script(
                "arguments[0].style.border='3px solid red'; arguments[0].style.backgroundColor='yellow';",
                element
            )
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
