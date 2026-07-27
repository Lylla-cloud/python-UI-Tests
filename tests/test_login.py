import pytest
from utils.config_reader import ConfigReader


class TestLogin:

    def test_successful_login(self, login_page):
        home = login_page.login(
            ConfigReader.get_nested("test_user", "email"),
            ConfigReader.get_nested("test_user", "password")
        )
        assert home.is_logged_in(), \
            "User should be logged in after valid credentials"
        assert ConfigReader.get_nested("test_user", "name") \
            in home.get_logged_in_username(), \
            "Logged in username should match"

    def test_failed_login_wrong_password(self, login_page):
        login_page.login("wronguser@test.com", "wrongpassword")
        assert login_page.is_displayed(login_page.LOGIN_ERROR), \
            "Error message should be displayed for invalid credentials"

    @pytest.mark.parametrize("email,password", [
        ("wronguser@test.com", "wrongpassword"),
        ("invalid-email", "password123"),
        ("test@test.com", "wrong"),
    ])
    def test_failed_login_scenarios(self, login_page, email, password):
        login_page.login(email, password)
        assert "login" in login_page.driver.current_url, \
            f"Should remain on login page for: {email}"

    def test_logout(self, home_page):
        login_page = home_page.go_to_signup_login()
        home = login_page.login(
            ConfigReader.get_nested("test_user", "email"),
            ConfigReader.get_nested("test_user", "password")
        )
        assert home.is_logged_in(), "Should be logged in first"
        home.logout()
        assert not home.is_logged_in(), \
            "Should be logged out after clicking logout"