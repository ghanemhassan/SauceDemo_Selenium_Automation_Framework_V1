"""
pages/base_page.py
───────────────────
Abstract base class for every Page Object in the framework.

All shared browser interactions live here so individual page classes
stay focused on their own locators and high-level actions.

Key responsibilities
--------------------
- Wrapping Selenium's explicit wait API (wait_for_element, etc.)
- Common navigation helpers (go_to, get_current_url, …)
- A centralised logger for every page
"""

import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

# Default explicit-wait timeout (seconds)
DEFAULT_TIMEOUT = 10


class BasePage:
    """Parent page object – inherit from this in every page class."""

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
        self.driver  = driver
        self.timeout = timeout
        self.wait    = WebDriverWait(driver, timeout)
        self.logger  = logging.getLogger(self.__class__.__name__)

    # ── Navigation ─────────────────────────────────────────────────────────────

    def go_to(self, url: str) -> None:
        """Navigate the browser to *url*."""
        self.logger.debug("Navigating to: %s", url)
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_title(self) -> str:
        return self.driver.title

    def refresh(self) -> None:
        self.driver.refresh()

    def go_back(self) -> None:
        self.driver.back()

    # ── Element retrieval (explicit waits) ─────────────────────────────────────

    def wait_for_element(
        self, locator: tuple, timeout: int | None = None
    ) -> WebElement:
        """Wait until an element is visible and return it."""
        t = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            self.logger.error(
                "Timed out waiting for element: %s (timeout=%ss)", locator, t
            )
            raise

    def wait_for_element_clickable(
        self, locator: tuple, timeout: int | None = None
    ) -> WebElement:
        """Wait until an element is clickable and return it."""
        t = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.element_to_be_clickable(locator)
            )
        except TimeoutException:
            self.logger.error(
                "Element not clickable: %s (timeout=%ss)", locator, t
            )
            raise

    def wait_for_element_present(
        self, locator: tuple, timeout: int | None = None
    ) -> WebElement:
        """Wait until an element exists in the DOM (not necessarily visible)."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.presence_of_element_located(locator)
        )

    def wait_for_elements(
        self, locator: tuple, timeout: int | None = None
    ) -> list[WebElement]:
        """Wait until at least one matching element is visible; return the list."""
        t = timeout or self.timeout
        return WebDriverWait(self.driver, t).until(
            EC.visibility_of_all_elements_located(locator)
        )

    def is_element_visible(self, locator: tuple, timeout: int = 3) -> bool:
        """Return True if the element becomes visible within *timeout* seconds."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def is_element_present(self, locator: tuple) -> bool:
        """Return True if the element exists in the DOM right now."""
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    # ── Interactions ───────────────────────────────────────────────────────────

    def click(self, locator: tuple) -> None:
        """Wait for element to be clickable, then click it."""
        self.logger.debug("Clicking: %s", locator)
        self.wait_for_element_clickable(locator).click()

    def type_text(self, locator: tuple, text: str, clear: bool = True) -> None:
        """Wait for element, optionally clear it, then send *text*."""
        self.logger.debug("Typing '%s' into: %s", text, locator)
        element = self.wait_for_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        """Return the visible text of an element."""
        return self.wait_for_element(locator).text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Return an HTML attribute value from an element."""
        return self.wait_for_element(locator).get_attribute(attribute) or ""

    def scroll_to_element(self, element: WebElement) -> None:
        """Scroll the element into the viewport."""
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    # ── URL / Title checks ─────────────────────────────────────────────────────

    def wait_for_url_contains(self, partial_url: str, timeout: int | None = None) -> bool:
        """Wait until the current URL contains *partial_url*."""
        t = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, t).until(
                EC.url_contains(partial_url)
            )
        except TimeoutException:
            self.logger.warning("URL did not contain '%s' within %ss", partial_url, t)
            return False
