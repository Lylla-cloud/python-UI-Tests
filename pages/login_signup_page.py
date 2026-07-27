from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginSignupPage(BasePage):

    # Login
    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR,
        "input[data-qa='login-password']")
    LOGIN_BTN = (By.CSS_SELECTOR,
        "button[data-qa='login-button']")
    LOGIN_ERROR = (By.XPATH,
        "//p[contains(text(),'Your email or password is incorrect')]")

    # Signup
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR,
        "input[data-qa='signup-email']")
    SIGNUP_BTN = (By.CSS_SELECTOR,
        "button[data-qa='signup-button']")
    EMAIL_EXISTS_ERROR = (By.XPATH,
        "//p[contains(text(),'Email Address already exist')]")

    def login(self, email, password):
        self.type(self.LOGIN_EMAIL, email)
        self.type(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BTN)
        from pages.home_page import HomePage
        return HomePage(self.driver)

    def signup(self, name, email):
        self.type(self.SIGNUP_NAME, name)
        self.type(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BTN)
        from pages.signup_form_page import SignupFormPage
        return SignupFormPage(self.driver)

    def get_login_error(self):
        return self.get_text(self.LOGIN_ERROR)

    def is_email_exists_error_displayed(self):
        return self.is_displayed(self.EMAIL_EXISTS_ERROR)