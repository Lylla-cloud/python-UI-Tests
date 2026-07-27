from behave import given, then
from pages.home_page import HomePage
from selenium.webdriver.support.ui import WebDriverWait

@given('I navigate to the Automation Exercise home page')
def step_impl(context):
    context.home_page = HomePage(context.driver)
    context.home_page.open()

@then('the page title should contain "{keyword}"')
def step_impl(context, keyword):
    # Wait up to 15 seconds for the page title to contain the keyword
    # to ensure the page has loaded on slow CI/CD pipelines
    WebDriverWait(context.driver, 15).until(
        lambda d: keyword in d.title
    )
    title = context.home_page.get_title()
    assert keyword in title, f"Expected '{keyword}' in title, but got '{title}'"
