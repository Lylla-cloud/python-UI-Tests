import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger("RenoDriverFactory")

class DriverFactory:
    @staticmethod
    def create_driver(browser: str = "chrome", headless: bool = True, timeout_seconds: int = 10) -> webdriver.Remote:
        browser_name = (browser or "chrome").lower().strip()
        
        if browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        else:
            # Default to Chrome
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--remote-allow-origins=*")
            options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        driver.implicitly_wait(timeout_seconds)
        driver.set_page_load_timeout(timeout_seconds * 2)
        driver.maximize_window()
        return driver
