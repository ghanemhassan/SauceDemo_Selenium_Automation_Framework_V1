"""
tests/test_login.py
────────────────────
Test suite for the SauceDemo Login page.

Test cases
──────────
TC_L01  Valid login with standard_user                  [smoke, login]
TC_L02  Invalid login – wrong password                  [regression, login]
TC_L03  Invalid login – wrong username                  [regression, login]
TC_L04  Login with empty username                       [regression, login]
TC_L05  Login with empty password                       [regression, login]
TC_L06  Login with both fields empty                    [regression, login]
TC_L07  Locked-out user sees specific error             [regression, login]
TC_L08  Error banner can be dismissed                   [regression, login]
TC_L09  Successful logout returns to login page         [smoke, login]
TC_L10  Page title is correct                           [smoke, login]
"""

import pytest
from pages.login_page     import LoginPage
from pages.inventory_page import InventoryPage


# ── Shared test data ───────────────────────────────────────────────────────────

VALID_USER     = "standard_user"
VALID_PASS     = "secret_sauce"
LOCKED_USER    = "locked_out_user"
INVALID_USER   = "invalid_user_xyz"
INVALID_PASS   = "wrong_password_123"
INVENTORY_URL  = "https://www.saucedemo.com/inventory.html"
BASE_URL       = "https://www.saucedemo.com/"


# ── Test class ────────────────────────────────────────────────────────────────

class TestLogin:
    """All login / authentication test cases."""

    # TC_L01 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.login
    def test_valid_login(self, driver):
        """Valid credentials navigate to the inventory page."""
        login_page = LoginPage(driver)
        login_page.login(VALID_USER, VALID_PASS)

        # Assert URL changed to inventory
        assert INVENTORY_URL in driver.current_url, (
            f"Expected URL to contain '{INVENTORY_URL}', got '{driver.current_url}'"
        )

        # Assert the inventory page title is rendered
        inventory_page = InventoryPage(driver)
        assert inventory_page.get_page_title_text() == "Products", (
            "Inventory page title should be 'Products'"
        )

    # TC_L02 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_password(self, driver):
        """Wrong password shows an appropriate error message."""
        login_page = LoginPage(driver)
        login_page.login(VALID_USER, INVALID_PASS)

        assert login_page.is_error_displayed(), "Error banner should be visible"
        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text, (
            f"Unexpected error message: {error_text}"
        )
        # URL should remain on the login page
        assert driver.current_url == BASE_URL, (
            f"Should stay on login page, got: {driver.current_url}"
        )

    # TC_L03 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.login
    def test_invalid_username(self, driver):
        """Wrong username shows an appropriate error message."""
        login_page = LoginPage(driver)
        login_page.login(INVALID_USER, VALID_PASS)

        assert login_page.is_error_displayed(), "Error banner should be visible"
        error_text = login_page.get_error_message()
        assert "Username and password do not match" in error_text, (
            f"Unexpected error message: {error_text}"
        )

    # TC_L04 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_username(self, driver):
        """Submitting with empty username shows a validation error."""
        login_page = LoginPage(driver)
        login_page.enter_password(VALID_PASS)
        login_page.click_login()

        assert login_page.is_error_displayed(), "Error banner should be visible"
        error_text = login_page.get_error_message()
        assert "Username is required" in error_text, (
            f"Expected username-required error, got: {error_text}"
        )

    # TC_L05 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.login
    def test_empty_password(self, driver):
        """Submitting with empty password shows a validation error."""
        login_page = LoginPage(driver)
        login_page.enter_username(VALID_USER)
        login_page.click_login()

        assert login_page.is_error_displayed(), "Error banner should be visible"
        error_text = login_page.get_error_message()
        assert "Password is required" in error_text, (
            f"Expected password-required error, got: {error_text}"
        )

    # TC_L06 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.login
    def test_both_fields_empty(self, driver):
        """Clicking Login with both fields empty shows a validation error."""
        login_page = LoginPage(driver)
        login_page.click_login()

        assert login_page.is_error_displayed(), "Error banner should be visible"
        error_text = login_page.get_error_message()
        assert "Username is required" in error_text, (
            f"Expected username-required error, got: {error_text}"
        )

    # TC_L07 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.login
    def test_locked_out_user(self, driver):
        """The locked_out_user account shows a specific lock-out message."""
        login_page = LoginPage(driver)
        login_page.login(LOCKED_USER, VALID_PASS)

        assert login_page.is_error_displayed(), "Error banner should be visible"
        error_text = login_page.get_error_message()
        assert "locked out" in error_text.lower(), (
            f"Expected locked-out message, got: {error_text}"
        )

    # TC_L08 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.login
    def test_error_banner_can_be_dismissed(self, driver):
        """Clicking the ✕ on the error banner hides it."""
        login_page = LoginPage(driver)
        login_page.login(INVALID_USER, INVALID_PASS)

        assert login_page.is_error_displayed(), "Error banner should appear after bad login"

        login_page.clear_error()

        assert not login_page.is_error_displayed(), (
            "Error banner should be hidden after clicking close"
        )

    # TC_L09 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.login
    def test_logout(self, logged_in):
        """After login, using the side menu to logout returns to login page."""
        inventory_page = InventoryPage(logged_in)
        inventory_page.logout()

        # After logout the URL should be back at the root login page
        assert logged_in.current_url == BASE_URL, (
            f"Expected login page URL after logout, got: {logged_in.current_url}"
        )

        # The login form should be visible again
        login_page = LoginPage(logged_in)
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON), (
            "Login button should be visible after logout"
        )

    # TC_L10 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.login
    def test_login_page_title(self, driver):
        """Browser tab title on the login page is 'Swag Labs'."""
        assert "Swag Labs" in driver.title, (
            f"Expected 'Swag Labs' in page title, got: '{driver.title}'"
        )
