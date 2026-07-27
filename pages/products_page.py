from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductsPage(BasePage):

    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BTN = (By.ID, "submit_search")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo h2")
    PRODUCTS_LIST = (By.CSS_SELECTOR, ".features_items .col-sm-4")
    PAGE_TITLE = (By.CSS_SELECTOR, ".features_items h2.title")

    def search(self, keyword):
        self.type(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BTN)
        return self

    def get_product_names(self):
        elements = self.find_all(self.PRODUCT_NAMES)
        return [e.text for e in elements]

    def get_product_count(self):
        try:
            elements = self.find_all(self.PRODUCTS_LIST)
            return len(elements)
        except Exception:
            return 0

    def is_page_loaded(self):
        return self.is_displayed(self.PAGE_TITLE)