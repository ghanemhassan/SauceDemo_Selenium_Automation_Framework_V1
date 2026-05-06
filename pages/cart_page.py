"""
pages/cart_page.py
───────────────────
Page Object for the SauceDemo Cart page.
URL: https://www.saucedemo.com/cart.html

Public methods
--------------
get_cart_items()            – list of item name strings in the cart
get_cart_item_count()       – number of rows in the cart
is_item_in_cart(name)       – True if the named item is listed
remove_item(name)           – click 'Remove' next to the named item
continue_shopping()         – click 'Continue Shopping' button
proceed_to_checkout()       – click 'Checkout' button
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates all interactions with the cart page."""

    URL = "https://www.saucedemo.com/cart.html"

    # ── Locators ───────────────────────────────────────────────────────────────

    PAGE_TITLE           = (By.CLASS_NAME, "title")
    CART_ITEMS           = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAMES      = (By.CLASS_NAME, "inventory_item_name")
    CART_ITEM_PRICES     = (By.CLASS_NAME, "inventory_item_price")
    CART_ITEM_QUANTITIES = (By.CLASS_NAME, "cart_quantity")

    CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    CHECKOUT_BTN          = (By.ID, "checkout")

    # ── Navigation ─────────────────────────────────────────────────────────────

    def open(self) -> "CartPage":
        self.go_to(self.URL)
        self.logger.info("Opened cart page directly")
        return self

    # ── Queries ────────────────────────────────────────────────────────────────

    def get_page_title_text(self) -> str:
        return self.get_text(self.PAGE_TITLE)

    def get_cart_items(self) -> list[str]:
        """Return list of item name strings currently in the cart."""
        if not self.is_element_visible(self.CART_ITEM_NAMES, timeout=3):
            return []
        elements = self.driver.find_elements(*self.CART_ITEM_NAMES)
        return [el.text for el in elements]

    def get_cart_item_count(self) -> int:
        """Return the number of distinct item rows in the cart."""
        if not self.is_element_visible(self.CART_ITEMS, timeout=3):
            return 0
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def is_item_in_cart(self, product_name: str) -> bool:
        """True if *product_name* appears in the cart's item list."""
        return product_name in self.get_cart_items()

    def get_item_quantity(self, product_name: str) -> int | None:
        """
        Return the quantity shown for a specific cart item.
        Returns None if the item is not found.
        """
        items = self.driver.find_elements(*self.CART_ITEMS)
        for item in items:
            name_el = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_el.text == product_name:
                qty_el = item.find_element(By.CLASS_NAME, "cart_quantity")
                return int(qty_el.text)
        return None

    # ── Remove item ────────────────────────────────────────────────────────────

    def remove_item(self, product_name: str) -> "CartPage":
        """Click the Remove button next to *product_name*."""
        self.logger.info("Removing from cart: %s", product_name)
        data_test_id = "remove-" + product_name.lower().replace(" ", "-")
        locator = (By.CSS_SELECTOR, f"[data-test='{data_test_id}']")
        self.click(locator)
        return self

    # ── Buttons ────────────────────────────────────────────────────────────────

    def continue_shopping(self) -> None:
        """Click the 'Continue Shopping' button (returns to inventory)."""
        self.logger.info("Clicking 'Continue Shopping'")
        self.click(self.CONTINUE_SHOPPING_BTN)

    def proceed_to_checkout(self) -> None:
        """Click the 'Checkout' button (navigates to checkout step 1)."""
        self.logger.info("Clicking 'Checkout'")
        self.click(self.CHECKOUT_BTN)
