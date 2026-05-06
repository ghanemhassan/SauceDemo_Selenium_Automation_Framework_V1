"""
tests/test_checkout.py
───────────────────────
Test suite for the SauceDemo Checkout flow (steps 1–3).

Test cases
──────────
TC_CH01  Checkout step-1 URL is correct                      [smoke, checkout]
TC_CH02  Cancel on step-1 returns to cart                    [regression, checkout]
TC_CH03  Empty first-name shows validation error             [regression, checkout]
TC_CH04  Empty last-name shows validation error              [regression, checkout]
TC_CH05  Empty zip code shows validation error               [regression, checkout]
TC_CH06  All fields empty shows validation error             [regression, checkout]
TC_CH07  Valid info advances to checkout step-2              [smoke, checkout]
TC_CH08  Step-2 overview lists ordered products              [regression, checkout]
TC_CH09  Step-2 shows item total, tax and grand total        [regression, checkout]
TC_CH10  Cancel on step-2 returns to inventory               [regression, checkout]
TC_CH11  Finish button completes the order                   [smoke, checkout]
TC_CH12  Completion page shows confirmation header           [smoke, checkout]
TC_CH13  Completion page shows success illustration          [regression, checkout]
TC_CH14  Back Home button returns to inventory               [regression, checkout]
TC_CH15  Full end-to-end order flow                          [smoke, checkout]
"""

import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page      import CartPage
from pages.checkout_page  import CheckoutPage


# ── Constants ──────────────────────────────────────────────────────────────────

PRODUCT_BACKPACK   = "Sauce Labs Backpack"
PRODUCT_BIKE_LIGHT = "Sauce Labs Bike Light"

CART_URL        = "https://www.saucedemo.com/cart.html"
CHECKOUT_S1_URL = "https://www.saucedemo.com/checkout-step-one.html"
CHECKOUT_S2_URL = "https://www.saucedemo.com/checkout-step-two.html"
CHECKOUT_OK_URL = "https://www.saucedemo.com/checkout-complete.html"
INVENTORY_URL   = "https://www.saucedemo.com/inventory.html"

VALID_FIRST = "Jane"
VALID_LAST  = "Doe"
VALID_ZIP   = "90210"


# ── Helper: reach checkout step 1 with one item in cart ───────────────────────

def _reach_checkout_step1(driver) -> CheckoutPage:
    """Add one product then navigate through to checkout step 1."""
    inventory = InventoryPage(driver)
    inventory.add_product_to_cart(PRODUCT_BACKPACK)
    inventory.open_cart()
    cart = CartPage(driver)
    cart.proceed_to_checkout()
    return CheckoutPage(driver)


# ── Test class ────────────────────────────────────────────────────────────────

class TestCheckout:
    """All checkout flow test cases."""

    # TC_CH01 ─────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_checkout_step1_url(self, logged_in):
        """Proceeding from cart lands on checkout-step-one.html."""
        checkout = _reach_checkout_step1(logged_in)
        assert CHECKOUT_S1_URL in logged_in.current_url, (
            f"Expected '{CHECKOUT_S1_URL}', got '{logged_in.current_url}'"
        )

    # TC_CH02 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_cancel_on_step1_returns_to_cart(self, logged_in):
        """Cancel on step-1 takes the user back to the cart page."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.click_cancel()

        assert CART_URL in logged_in.current_url, (
            f"Expected cart URL after cancel, got '{logged_in.current_url}'"
        )

    # TC_CH03 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_empty_first_name_shows_error(self, logged_in):
        """Submitting step-1 without first name shows a validation error."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.enter_last_name(VALID_LAST)
        checkout.enter_zip_code(VALID_ZIP)
        checkout.click_continue()

        assert checkout.is_error_displayed(), "Error should appear when first name is empty"
        assert "First Name is required" in checkout.get_error_message(), (
            f"Unexpected error: {checkout.get_error_message()}"
        )

    # TC_CH04 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_empty_last_name_shows_error(self, logged_in):
        """Submitting step-1 without last name shows a validation error."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.enter_first_name(VALID_FIRST)
        checkout.enter_zip_code(VALID_ZIP)
        checkout.click_continue()

        assert checkout.is_error_displayed(), "Error should appear when last name is empty"
        assert "Last Name is required" in checkout.get_error_message(), (
            f"Unexpected error: {checkout.get_error_message()}"
        )

    # TC_CH05 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_empty_zip_shows_error(self, logged_in):
        """Submitting step-1 without zip code shows a validation error."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.enter_first_name(VALID_FIRST)
        checkout.enter_last_name(VALID_LAST)
        checkout.click_continue()

        assert checkout.is_error_displayed(), "Error should appear when zip code is empty"
        assert "Postal Code is required" in checkout.get_error_message(), (
            f"Unexpected error: {checkout.get_error_message()}"
        )

    # TC_CH06 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_all_fields_empty_shows_error(self, logged_in):
        """Submitting step-1 with all fields empty shows a validation error."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.click_continue()

        assert checkout.is_error_displayed(), (
            "Error should appear when all fields are empty"
        )

    # TC_CH07 ─────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_valid_info_advances_to_step2(self, logged_in):
        """Completing step-1 with valid data navigates to step-2 overview."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)

        assert CHECKOUT_S2_URL in logged_in.current_url, (
            f"Expected step-2 URL, got '{logged_in.current_url}'"
        )

    # TC_CH08 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_step2_lists_ordered_products(self, logged_in):
        """Order overview on step-2 lists all products from the cart."""
        inventory = InventoryPage(logged_in)
        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.add_product_to_cart(PRODUCT_BIKE_LIGHT)
        inventory.open_cart()
        cart = CartPage(logged_in)
        cart.proceed_to_checkout()
        checkout = CheckoutPage(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)

        overview_items = checkout.get_overview_item_names()
        assert PRODUCT_BACKPACK   in overview_items, "Backpack missing from overview"
        assert PRODUCT_BIKE_LIGHT in overview_items, "Bike Light missing from overview"

    # TC_CH09 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_step2_shows_price_summary(self, logged_in):
        """Order overview displays item total, tax, and grand total labels."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)

        assert "Item total:" in checkout.get_item_total(), "Item total label missing"
        assert "Tax:"        in checkout.get_tax(),        "Tax label missing"
        assert "Total:"      in checkout.get_order_total(),"Grand total label missing"

    # TC_CH10 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_cancel_on_step2_returns_to_inventory(self, logged_in):
        """Cancel on step-2 overview navigates back to the inventory page."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)

        # Use the cancel locator defined for step-2 (same ID as step-1)
        checkout.click_cancel()

        assert INVENTORY_URL in logged_in.current_url, (
            f"Expected inventory URL after step-2 cancel, got '{logged_in.current_url}'"
        )

    # TC_CH11 ─────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_finish_completes_the_order(self, logged_in):
        """Clicking Finish on step-2 navigates to the completion page."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)
        checkout.click_finish()

        assert CHECKOUT_OK_URL in logged_in.current_url, (
            f"Expected completion URL '{CHECKOUT_OK_URL}', got '{logged_in.current_url}'"
        )

    # TC_CH12 ─────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_completion_page_shows_thank_you_header(self, logged_in):
        """Completion page header contains a thank-you message."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)
        checkout.click_finish()

        assert checkout.is_order_complete(), "Completion page header should be visible"
        header = checkout.get_confirmation_header()
        assert "Thank you" in header, (
            f"Expected 'Thank you' in header, got '{header}'"
        )

    # TC_CH13 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_completion_page_shows_success_image(self, logged_in):
        """The success illustration (pony_express) is displayed on completion."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)
        checkout.click_finish()

        assert checkout.is_pony_express_displayed(), (
            "Success illustration should be visible on the completion page"
        )

    # TC_CH14 ─────────────────────────────────────────────────────────────────
    @pytest.mark.regression
    @pytest.mark.checkout
    def test_back_home_returns_to_inventory(self, logged_in):
        """'Back Home' on the completion page navigates to the inventory."""
        checkout = _reach_checkout_step1(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)
        checkout.click_finish()
        checkout.click_back_home()

        assert INVENTORY_URL in logged_in.current_url, (
            f"Expected inventory URL, got '{logged_in.current_url}'"
        )

    # TC_CH15 ─────────────────────────────────────────────────────────────────
    @pytest.mark.smoke
    @pytest.mark.checkout
    def test_full_end_to_end_purchase_flow(self, logged_in):
        """
        Full happy-path: login → add two items → cart → checkout → confirm.
        This is the most important smoke test in the suite.
        """
        # Step 1 – Add products from inventory
        inventory = InventoryPage(logged_in)
        inventory.add_product_to_cart(PRODUCT_BACKPACK)
        inventory.add_product_to_cart(PRODUCT_BIKE_LIGHT)
        assert inventory.get_cart_badge_count() == 2, "Badge should show 2"

        # Step 2 – Navigate to cart and verify products
        inventory.open_cart()
        cart = CartPage(logged_in)
        assert cart.is_item_in_cart(PRODUCT_BACKPACK),   "Backpack missing from cart"
        assert cart.is_item_in_cart(PRODUCT_BIKE_LIGHT), "Bike Light missing from cart"

        # Step 3 – Checkout: customer information
        cart.proceed_to_checkout()
        checkout = CheckoutPage(logged_in)
        checkout.complete_checkout_information(VALID_FIRST, VALID_LAST, VALID_ZIP)
        assert CHECKOUT_S2_URL in logged_in.current_url, "Should be on step-2"

        # Step 4 – Verify order summary and complete
        assert PRODUCT_BACKPACK   in checkout.get_overview_item_names()
        assert PRODUCT_BIKE_LIGHT in checkout.get_overview_item_names()
        checkout.click_finish()

        # Step 5 – Confirm order completion
        assert checkout.is_order_complete(), "Order completion page should be shown"
        assert "Thank you" in checkout.get_confirmation_header()
        assert CHECKOUT_OK_URL in logged_in.current_url
