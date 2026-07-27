import pytest


class TestProducts:

    def test_all_products_page_loads(self, products_page):
        assert products_page.is_page_loaded(), \
            "Products page should load successfully"
        assert products_page.get_product_count() > 0, \
            "Products page should display products"

    def test_product_search(self, products_page):
        products_page.search("dress")
        assert products_page.get_product_count() > 0, \
            "Search should return results for 'dress'"

    @pytest.mark.parametrize("keyword", [
        "top", "dress", "jeans", "saree"
    ])
    def test_search_various_products(self, products_page, keyword):
        products_page.search(keyword)
        assert products_page.get_product_count() > 0, \
            f"Search for '{keyword}' should return results"

    def test_search_nonexistent_product(self, products_page):
        products_page.search("xyznonexistentproduct123")
        assert products_page.get_product_count() == 0, \
            "Search for non-existent product should return 0 results"