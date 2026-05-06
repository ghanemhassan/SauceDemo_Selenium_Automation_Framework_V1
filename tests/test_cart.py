"""
tests/test_cart.py
───────────────────
Test suite for the SauceDemo Shopping Cart page.

Test cases
──────────
TC_C01  Navigating to cart shows 'Your Cart' title           [smoke, cart]
TC_C02  Cart URL is correct                                  [smoke, cart]
TC_C03  Added product appears in the cart                    [smoke, cart]
TC_C04  Multiple added products all appear in the cart       [regression, cart]
TC_C05  Item quantity in cart defaults to 1                  [regression, cart]
TC_C06  Remove item from cart page                           [regression, cart]
TC_C07  Cart is empty after removing all items               [regression, cart]
TC_C08  'Continue Shopping' returns to inventory             [regression, cart]
TC_C09  'Checkout' button navigates to checkout step 1       [smoke, cart]
TC_C10  Cart icon on inventory navigates to cart page        [smoke, cart]
"""

import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page      import CartPage
from pages.checkout_page  import CheckoutPage


PRODUCT_BACKPACK   = "Sauce Labs Backpack"
PRODUCT_BIKE_LIGHT = "Sauce Labs Bike Light"
PRODUCT_ONESIE     = "Sauce Labs Onesie"

CART_URL       = "https://www.saucedemo.com/cart.html"
INVENTORY_URL  = "https://www.saucedemo.com/inventory.html"
CHECKOUT_URL   = "https://www.saucedemo.com/checkout-step-one.html"


class TestCart:
    """All shopping cart test cases."""

    # TC_C01 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_page_title(self, logged_in):
        """Cart page heading reads 'Your Cart'."""
        inventory = InventoryPage(logged_in)
        inventory.open_cart()

        cart = CartPage(logged_in)
        assert cart.get_page_title_text() == "Your Cart", (
            f"Expected 'Your Cart', got '{cart.get_page_title_text()}'"
        )

    # TC_C02 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_url(self, logged_in):
        """Clicking cart icon navigates to /cart.html."""
        inventory = InventoryPage(logged_in)
        inventory.open_cart()

        assert CART_URL in logged_in.current_url, (
            f"Expected cart URL '{CART_URL}', got '{logged_in.current_url}'"
        )

    # TC_C03 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_added_product_appears_in_cart(self, logged_in):
        """A product added from inventory is listed on the cart page."""
        inventory = InventoryPage(logged_in)
        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.open_cart()

        cart = CartPage(logged_in)
        assert cart.is_item_in_cart(PRODUCT_BACKPACK), (
            f"'{PRODUCT_BACKPACK}' should appear in the cart"
        )

    # TC_C04 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.cart
    def test_multiple_products_in_cart(self, logged_in):
        """All products added from inventory appear on the cart page."""
        inventory = InventoryPage(logged_in)
        products = [PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT, PRODUCT_ONESIE]
        for p in products:
            inventory.add_product_to_cart(p)
        inventory.open_cart()

        cart = CartPage(logged_in)
        assert cart.get_cart_item_count() == len(products), (
            f"Expected {len(products)} items in cart, got {cart.get_cart_item_count()}"
        )
        for p in products:
            assert cart.is_item_in_cart(p), f"'{p}' not found in cart"

    # TC_C05 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.cart
    def test_item_quantity_defaults_to_one(self, logged_in):
        """Each product added once should show quantity 1 in the cart."""
        inventory = InventoryPage(logged_in)
        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.open_cart()

        cart = CartPage(logged_in)
        qty = cart.get_item_quantity(PRODUCT_BACKPACK)
        assert qty == 1, f"Expected quantity 1 for '{PRODUCT_BACKPACK}', got {qty}"

    # TC_C06 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.cart
    def test_remove_item_from_cart_page(self, logged_in):
        """Removing an item from the cart page makes it disappear from the list."""
        inventory = InventoryPage(logged_in)
        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.add_product_to_cart(PRODUCT_BIKE_LIGHT)
        inventory.open_cart()

        cart = CartPage(logged_in)
        assert cart.is_item_in_cart(PRODUCT_BACKPACK), "Item should be in cart before removal"

        cart.remove_item(PRODUCT_BACKPACK)

        assert not cart.is_item_in_cart(PRODUCT_BACKPACK), (
            "Removed item should no longer appear in cart"
        )
        # The other item should still be there
        assert cart.is_item_in_cart(PRODUCT_BIKE_LIGHT), (
            "Other items should remain in cart after one is removed"
        )

    # TC_C07 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.cart
    def test_cart_empty_after_removing_all_items(self, logged_in):
        """Removing all items leaves the cart with 0 items."""
        inventory = InventoryPage(logged_in)
        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.open_cart()

        cart = CartPage(logged_in)
        cart.remove_item(PRODUCT_BACKPACK)

        assert cart.get_cart_item_count() == 0, (
            "Cart should have 0 items after removing the only item"
        )

    # TC_C08 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.cart
    def test_continue_shopping_returns_to_inventory(self, logged_in):
        """'Continue Shopping' button takes the user back to the inventory."""
        inventory = InventoryPage(logged_in)
        inventory.open_cart()

        cart = CartPage(logged_in)
        cart.continue_shopping()

        assert INVENTORY_URL in logged_in.current_url, (
            f"Expected inventory URL after 'Continue Shopping', got '{logged_in.current_url}'"
        )

    # TC_C09 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_checkout_button_navigates_to_checkout(self, logged_in):
        """'Checkout' button navigates to checkout step 1."""
        inventory = InventoryPage(logged_in)
        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.open_cart()

        cart = CartPage(logged_in)
        cart.proceed_to_checkout()

        assert CHECKOUT_URL in logged_in.current_url, (
            f"Expected checkout URL '{CHECKOUT_URL}', got '{logged_in.current_url}'"
        )

    # TC_C10 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.cart
    def test_cart_icon_opens_cart(self, logged_in):
        """Cart icon on the inventory page navigates to /cart.html."""
        inventory = InventoryPage(logged_in)
        inventory.open_cart()

        assert CART_URL in logged_in.current_url, (
            f"Expected '{CART_URL}', got '{logged_in.current_url}'"
        )
