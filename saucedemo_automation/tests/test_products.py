"""
tests/test_products.py
───────────────────────
Test suite for the SauceDemo Inventory / Products page.

Test cases
──────────
TC_P01  Products page loads with 6 products              [smoke, products]
TC_P02  Page title is 'Products'                         [smoke, products]
TC_P03  Add a single product to the cart                 [smoke, products]
TC_P04  Cart badge increments for each added product     [regression, products]
TC_P05  Add multiple products and verify badge count     [regression, products]
TC_P06  Remove a product from the inventory page         [regression, products]
TC_P07  Cart badge disappears when cart is empty         [regression, products]
TC_P08  Products can be sorted A→Z (default)             [regression, products]
TC_P09  Products can be sorted Z→A                       [regression, products]
TC_P10  Products can be sorted low-to-high price         [regression, products]
TC_P11  Products can be sorted high-to-low price         [regression, products]
"""

import pytest
from pages.inventory_page import InventoryPage


# ── Shared constants ───────────────────────────────────────────────────────────

PRODUCT_BACKPACK   = "Sauce Labs Backpack"
PRODUCT_BIKE_LIGHT = "Sauce Labs Bike Light"
PRODUCT_BOLT_SHIRT = "Sauce Labs Bolt T-Shirt"
EXPECTED_PRODUCT_COUNT = 6


class TestProducts:
    """All product catalogue / inventory page test cases."""

    # TC_P01 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.products
    def test_product_list_loads(self, logged_in):
        """Inventory page displays exactly 6 products after login."""
        inventory = InventoryPage(logged_in)
        count = inventory.get_product_count()
        assert count == EXPECTED_PRODUCT_COUNT, (
            f"Expected {EXPECTED_PRODUCT_COUNT} products, found {count}"
        )

    # TC_P02 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.products
    def test_page_title_is_products(self, logged_in):
        """The inventory page heading reads 'Products'."""
        inventory = InventoryPage(logged_in)
        title = inventory.get_page_title_text()
        assert title == "Products", (
            f"Expected page title 'Products', got '{title}'"
        )

    # TC_P03 ──────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.products
    def test_add_single_product_to_cart(self, logged_in):
        """Adding one product increments the cart badge to 1."""
        inventory = InventoryPage(logged_in)

        # Cart badge should not be visible before adding anything
        assert not inventory.is_cart_badge_visible(), (
            "Cart badge should be absent before adding items"
        )

        inventory.add_product_to_cart(PRODUCT_BACKPACK)

        badge_count = inventory.get_cart_badge_count()
        assert badge_count == 1, (
            f"Cart badge should show 1, got {badge_count}"
        )

    # TC_P04 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_cart_badge_increments_per_product(self, logged_in):
        """Cart badge number increases by 1 for each product added."""
        inventory = InventoryPage(logged_in)

        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        assert inventory.get_cart_badge_count() == 1, "Badge should be 1 after first add"

        inventory.add_product_to_cart(PRODUCT_BIKE_LIGHT)
        assert inventory.get_cart_badge_count() == 2, "Badge should be 2 after second add"

    # TC_P05 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_add_multiple_products(self, logged_in):
        """Adding three products shows badge count of 3."""
        inventory = InventoryPage(logged_in)

        products_to_add = [PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT, PRODUCT_BOLT_SHIRT]
        for product in products_to_add:
            inventory.add_product_to_cart(product)

        badge_count = inventory.get_cart_badge_count()
        assert badge_count == len(products_to_add), (
            f"Expected badge count {len(products_to_add)}, got {badge_count}"
        )

    # TC_P06 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_remove_product_from_inventory_page(self, logged_in):
        """After adding and removing a product, the cart badge decrements."""
        inventory = InventoryPage(logged_in)

        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        assert inventory.get_cart_badge_count() == 1, "Badge should be 1 after adding"

        inventory.remove_product(PRODUCT_BACKPACK)
        assert inventory.get_cart_badge_count() == 0, (
            "Badge count should be 0 after removing the only item"
        )

    # TC_P07 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_cart_badge_disappears_when_empty(self, logged_in):
        """The cart badge element is not rendered when the cart is empty."""
        inventory = InventoryPage(logged_in)

        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.remove_product(PRODUCT_BACKPACK)

        assert not inventory.is_cart_badge_visible(), (
            "Cart badge should not be visible when cart is empty"
        )

    # TC_P08 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_sort_products_az(self, logged_in):
        """Sorting A→Z returns products in ascending alphabetical order."""
        inventory = InventoryPage(logged_in)
        inventory.sort_products(InventoryPage.SORT_AZ)

        names = inventory.get_product_names()
        assert names == sorted(names), (
            f"Products should be in A→Z order. Got: {names}"
        )

    # TC_P09 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_sort_products_za(self, logged_in):
        """Sorting Z→A returns products in descending alphabetical order."""
        inventory = InventoryPage(logged_in)
        inventory.sort_products(InventoryPage.SORT_ZA)

        names = inventory.get_product_names()
        assert names == sorted(names, reverse=True), (
            f"Products should be in Z→A order. Got: {names}"
        )

    # TC_P10 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_sort_products_low_to_high(self, logged_in):
        """Sorting low-to-high returns prices in ascending order."""
        inventory = InventoryPage(logged_in)
        inventory.sort_products(InventoryPage.SORT_LOHI)

        prices = inventory.get_product_prices()
        assert prices == sorted(prices), (
            f"Prices should be ascending. Got: {prices}"
        )

    # TC_P11 ──────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.products
    def test_sort_products_high_to_low(self, logged_in):
        """Sorting high-to-low returns prices in descending order."""
        inventory = InventoryPage(logged_in)
        inventory.sort_products(InventoryPage.SORT_HILO)

        prices = inventory.get_product_prices()
        assert prices == sorted(prices, reverse=True), (
            f"Prices should be descending. Got: {prices}"
        )
