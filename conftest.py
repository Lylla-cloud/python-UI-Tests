import pytest
from core.driver_factory import DriverFactory

def pytest_addoption(parser):
    parser.addoption("--target-url", action="store", default="https://example.com", help="Target URL for testing")
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome or firefox")
    parser.addoption("--headless", action="store_true", default=True, help="Run browser in headless mode")
    parser.addoption("--timeout", action="store", default=10, type=int, help="Implicit wait timeout in seconds")

@pytest.fixture(scope="session")
def target_url(request):
    url = request.config.getoption("--target-url")
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    timeout = request.config.getoption("--timeout")
    
    driver_instance = DriverFactory.create_driver(browser=browser, headless=headless, timeout_seconds=timeout)
    yield driver_instance
    try:
        driver_instance.quit()
    except Exception:
        pass
