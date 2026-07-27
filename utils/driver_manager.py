import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from utils.config_reader import ConfigReader


def get_driver():
    browser = ConfigReader.get("browser", "chrome")
    headless = ConfigReader.get("headless", True)
    remote_url = os.environ.get("SELENIUM_REMOTE_URL")

    if remote_url:
        from selenium.webdriver import Remote
        options = ChromeOptions()
        options.add_argument("--headless")
        return Remote(command_executor=remote_url, options=options)

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        service = ChromeService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser}")