import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_manager import get_driver
from utils.config_reader import ConfigReader

def pytest_addoption(parser):
    parser.addoption("--browser", action="store",
                     default=None,
                     help="Browser: chrome or firefox")

@pytest.fixture(scope="session")
def config():
    return ConfigReader.get_config()

@pytest.fixture(scope="session")
def target_url():
    return ConfigReader.get("base_url")

@pytest.fixture
def driver(request):
    d = get_driver()
    yield d
    d.quit()

@pytest.fixture
def home_page(driver):
    from pages.home_page import HomePage
    page = HomePage(driver)
    page.open()
    return page

@pytest.fixture
def login_page(home_page):
    return home_page.go_to_signup_login()

@pytest.fixture
def products_page(home_page):
    return home_page.go_to_products()
