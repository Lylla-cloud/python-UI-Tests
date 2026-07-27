from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class HomePage(BasePage):

    SIGNUP_LOGIN_BTN = (By.PARTIAL_LINK_TEXT, "Signup / Login")
    PRODUCTS_BTN = (By.PARTIAL_LINK_TEXT, "Products")
    CART_BTN = (By.PARTIAL_LINK_TEXT, "Cart")
    LOGGED_IN_AS = (By.XPATH,
        "//a[contains(text(), 'Logged in as')]")
    LOGOUT_BTN = (By.PARTIAL_LINK_TEXT, "Logout")
    CONTACT_US_BTN = (By.PARTIAL_LINK_TEXT, "Contact us")

    def open(self):
        self.driver.get(ConfigReader.get("base_url"))
        return self

    def go_to_signup_login(self):
        self.click(self.SIGNUP_LOGIN_BTN)
        from pages.login_signup_page import LoginSignupPage
        return LoginSignupPage(self.driver)

    def go_to_products(self):
        self.click(self.PRODUCTS_BTN)
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)

    def is_logged_in(self):
        return self.is_displayed(self.LOGGED_IN_AS)

    def get_logged_in_username(self):
        return self.get_text(self.LOGGED_IN_AS)

    def logout(self):
        self.click(self.LOGOUT_BTN)
        return self

    def get_title(self):
        return self.driver.title