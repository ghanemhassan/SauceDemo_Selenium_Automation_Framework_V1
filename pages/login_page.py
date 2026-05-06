"""
pages/login_page.py
────────────────────
Page Object for the SauceDemo Login page (https://www.saucedemo.com/).

Locators
--------
All locators are defined as class-level tuples (By.*, "selector") so they
are easy to update when the UI changes.

Public methods
--------------
login(username, password)  – complete the login form and submit
get_error_message()        – return the text of any inline error banner
is_error_displayed()       – True/False visibility check on the error banner
clear_error()              – click the ✕ button that dismisses the banner
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates all interactions with the login page."""

    # ── URL ────────────────────────────────────────────────────────────────────
    URL = "https://www.saucedemo.com/"

    # ── Locators ───────────────────────────────────────────────────────────────
    # Input fields
    USERNAME_INPUT  = (By.ID, "user-name")
    PASSWORD_INPUT  = (By.ID, "password")

    # Buttons
    LOGIN_BUTTON    = (By.ID, "login-button")

    # Error container
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_CLOSE_BTN = (By.CSS_SELECTOR, ".error-button")

    # Header visible after successful login
    APP_LOGO        = (By.CLASS_NAME, "app_logo")

    # ── Actions ────────────────────────────────────────────────────────────────

    def open(self) -> "LoginPage":
        """Navigate directly to the login page."""
        self.go_to(self.URL)
        self.logger.info("Opened login page: %s", self.URL)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Type *username* into the username field."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Type *password* into the password field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        """Click the Login button."""
        self.click(self.LOGIN_BUTTON)
        self.logger.info("Clicked Login button")

    def login(self, username: str, password: str) -> None:
        """
        Complete the full login flow.

        Parameters
        ----------
        username : credential username
        password : credential password
        """
        self.logger.info("Logging in as '%s'", username)
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    # ── Assertions / queries ───────────────────────────────────────────────────

    def get_error_message(self) -> str:
        """Return the text of the red error banner (raises if not visible)."""
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        """True if the error banner is currently visible on the page."""
        return self.is_element_visible(self.ERROR_MESSAGE)

    def clear_error(self) -> "LoginPage":
        """Click the ✕ button to dismiss the error banner."""
        self.click(self.ERROR_CLOSE_BTN)
        return self

    def is_logged_in(self) -> bool:
        """True if the app logo (post-login header) is visible."""
        return self.is_element_visible(self.APP_LOGO)

    def get_username_field_value(self) -> str:
        """Return the current value inside the username input."""
        return self.get_attribute(self.USERNAME_INPUT, "value")

    def get_password_field_value(self) -> str:
        """Return the current value inside the password input."""
        return self.get_attribute(self.PASSWORD_INPUT, "value")
