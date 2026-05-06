"""
pages/inventory_page.py
────────────────────────
Page Object for the SauceDemo Inventory / Products page.
URL pattern: https://www.saucedemo.com/inventory.html

Public methods
--------------
get_product_names()          – list of all visible product names
get_product_count()          – how many products are on the page
add_product_to_cart(name)    – click "Add to cart" for a specific product
remove_product(name)         – click "Remove" for a specific product
get_cart_badge_count()       – integer value shown on the cart icon badge
sort_products(option)        – select a sort option from the dropdown
open_cart()                  – click the shopping cart icon
open_burger_menu()           – open the hamburger / side navigation menu
logout()                     – navigate through the side menu to logout
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Encapsulates all interactions with the products/inventory page."""

    URL = "https://www.saucedemo.com/inventory.html"

    # ── Locators ───────────────────────────────────────────────────────────────

    # Page-level
    PAGE_TITLE          = (By.CLASS_NAME, "title")
    PRODUCT_SORT_SELECT = (By.CLASS_NAME, "product_sort_container")

    # Product list
    PRODUCT_ITEMS       = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES       = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES      = (By.CLASS_NAME, "inventory_item_price")

    # Cart
    CART_ICON           = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE          = (By.CLASS_NAME, "shopping_cart_badge")

    # Burger / side menu
    BURGER_MENU_BTN     = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK         = (By.ID, "logout_sidebar_link")
    CLOSE_MENU_BTN      = (By.ID, "react-burger-cross-btn")

    # Sort options (text values used with Select)
    SORT_AZ   = "az"
    SORT_ZA   = "za"
    SORT_LOHI = "lohi"
    SORT_HILO = "hilo"

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open(self) -> "InventoryPage":
        self.go_to(self.URL)
        self.logger.info("Opened inventory page")
        return self

    # ── Product queries ────────────────────────────────────────────────────────

    def get_page_title_text(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_product_names(self) -> list[str]:
        """Return a list of all product name strings visible on the page."""
        elements = self.wait_for_elements(self.PRODUCT_NAMES)
        return [el.text for el in elements]

    def get_product_count(self) -> int:
        """Return the number of product cards rendered on the page."""
        elements = self.wait_for_elements(self.PRODUCT_ITEMS)
        return len(elements)

    def get_product_prices(self) -> list[float]:
        """Return a list of product prices as floats (e.g. 9.99)."""
        elements = self.wait_for_elements(self.PRODUCT_PRICES)
        return [float(el.text.replace("$", "")) for el in elements]

    # ── Cart interactions ──────────────────────────────────────────────────────

    def _get_add_button_for(self, product_name: str):
        """
        Locate the 'Add to cart' button for a product by its display name.
        Converts the name to the data-test id format used by SauceDemo.
        E.g. 'Sauce Labs Backpack' → 'add-to-cart-sauce-labs-backpack'
        """
        data_test_id = (
            "add-to-cart-" + product_name.lower().replace(" ", "-")
        )
        locator = (By.CSS_SELECTOR, f"[data-test='{data_test_id}']")
        return self.wait_for_element_clickable(locator)

    def _get_remove_button_for(self, product_name: str):
        """Locate the 'Remove' button for a product by its display name."""
        data_test_id = (
            "remove-" + product_name.lower().replace(" ", "-")
        )
        locator = (By.CSS_SELECTOR, f"[data-test='{data_test_id}']")
        return self.wait_for_element_clickable(locator)

    def add_product_to_cart(self, product_name: str) -> "InventoryPage":
        """Click 'Add to cart' for the named product."""
        self.logger.info("Adding to cart: %s", product_name)
        self._get_add_button_for(product_name).click()
        return self

    def remove_product(self, product_name: str) -> "InventoryPage":
        """Click 'Remove' for the named product."""
        self.logger.info("Removing from cart: %s", product_name)
        self._get_remove_button_for(product_name).click()
        return self

    def get_cart_badge_count(self) -> int:
        """
        Return the integer shown on the cart badge.
        Returns 0 when the badge is not visible (empty cart).
        """
        if self.is_element_visible(self.CART_BADGE, timeout=2):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def is_cart_badge_visible(self) -> bool:
        return self.is_element_visible(self.CART_BADGE, timeout=2)

    def open_cart(self) -> None:
        """Click the cart icon to navigate to the cart page."""
        self.logger.info("Opening shopping cart")
        self.click(self.CART_ICON)

    # ── Sorting ────────────────────────────────────────────────────────────────

    def sort_products(self, option: str) -> "InventoryPage":
        """
        Select a sort option from the dropdown.

        Parameters
        ----------
        option : 'az' | 'za' | 'lohi' | 'hilo'
        """
        self.logger.info("Sorting products by: %s", option)
        select_element = self.wait_for_element(self.PRODUCT_SORT_SELECT)
        Select(select_element).select_by_value(option)
        return self

    # ── Burger menu / logout ───────────────────────────────────────────────────

    def open_burger_menu(self) -> "InventoryPage":
        self.click(self.BURGER_MENU_BTN)
        return self

    def close_burger_menu(self) -> "InventoryPage":
        self.click(self.CLOSE_MENU_BTN)
        return self

    def logout(self) -> None:
        """Open the side menu and click Logout."""
        self.logger.info("Logging out via burger menu")
        self.open_burger_menu()
        self.click(self.LOGOUT_LINK)
