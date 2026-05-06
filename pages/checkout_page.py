"""
pages/checkout_page.py
───────────────────────
Page Object covering the three-step SauceDemo checkout flow.

Step 1 – Checkout: Your Information  (checkout-step-one.html)
Step 2 – Checkout: Overview          (checkout-step-two.html)
Step 3 – Checkout: Complete!         (checkout-complete.html)

Public methods
--------------
fill_information(first, last, zip) – fill step-1 form and continue
click_continue()                   – submit step-1 form
click_cancel()                     – cancel (returns to cart or inventory)
click_finish()                     – complete the order on step-2
get_error_message()                – error text if form validation fails
is_order_complete()                – True when on the completion page
get_confirmation_header()          – "THANK YOU FOR YOUR ORDER" text
get_order_total()                  – "$X.XX" string from step-2
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Encapsulates all interactions with the checkout flow (steps 1-3)."""

    # ── URLs ───────────────────────────────────────────────────────────────────
    URL_STEP_ONE  = "https://www.saucedemo.com/checkout-step-one.html"
    URL_STEP_TWO  = "https://www.saucedemo.com/checkout-step-two.html"
    URL_COMPLETE  = "https://www.saucedemo.com/checkout-complete.html"

    # ── Step 1 locators ────────────────────────────────────────────────────────
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT  = (By.ID, "last-name")
    ZIP_CODE_INPUT   = (By.ID, "postal-code")
    CONTINUE_BTN     = (By.ID, "continue")
    CANCEL_BTN       = (By.ID, "cancel")
    ERROR_MESSAGE    = (By.CSS_SELECTOR, "h3[data-test='error']")
    ERROR_CLOSE_BTN  = (By.CSS_SELECTOR, ".error-button")

    # ── Step 2 locators ────────────────────────────────────────────────────────
    CART_ITEM_NAMES  = (By.CLASS_NAME, "inventory_item_name")
    ITEM_TOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL        = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL      = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN       = (By.ID, "finish")
    CANCEL_BTN_S2    = (By.ID, "cancel")

    # ── Step 3 locators ────────────────────────────────────────────────────────
    COMPLETE_HEADER  = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT    = (By.CLASS_NAME, "complete-text")
    BACK_HOME_BTN    = (By.ID, "back-to-products")
    PONY_EXPRESS_IMG = (By.CLASS_NAME, "pony_express")

    # ── Step 1 actions ─────────────────────────────────────────────────────────

    def enter_first_name(self, first_name: str) -> "CheckoutPage":
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str) -> "CheckoutPage":
        self.type_text(self.LAST_NAME_INPUT, last_name)
        return self

    def enter_zip_code(self, zip_code: str) -> "CheckoutPage":
        self.type_text(self.ZIP_CODE_INPUT, zip_code)
        return self

    def click_continue(self) -> None:
        self.logger.info("Clicking Continue on checkout step 1")
        self.click(self.CONTINUE_BTN)

    def click_cancel(self) -> None:
        self.logger.info("Clicking Cancel")
        self.click(self.CANCEL_BTN)

    def fill_information(
        self, first_name: str, last_name: str, zip_code: str
    ) -> "CheckoutPage":
        """
        Fill all three fields in the checkout information form.
        Does NOT click Continue – call click_continue() separately if needed,
        or use complete_checkout_information() for the full step.
        """
        self.logger.info(
            "Filling checkout info: %s %s, ZIP=%s", first_name, last_name, zip_code
        )
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_zip_code(zip_code)
        return self

    def complete_checkout_information(
        self, first_name: str, last_name: str, zip_code: str
    ) -> None:
        """Fill the form AND click Continue in a single call."""
        self.fill_information(first_name, last_name, zip_code)
        self.click_continue()

    # ── Error handling (step 1) ────────────────────────────────────────────────

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_element_visible(self.ERROR_MESSAGE, timeout=3)

    def close_error(self) -> "CheckoutPage":
        self.click(self.ERROR_CLOSE_BTN)
        return self

    # ── Step 2 actions ─────────────────────────────────────────────────────────

    def get_overview_item_names(self) -> list[str]:
        """Return names of products listed in the order summary."""
        elements = self.wait_for_elements(self.CART_ITEM_NAMES)
        return [el.text for el in elements]

    def get_item_total(self) -> str:
        """Return subtotal label text, e.g. 'Item total: $39.99'."""
        return self.get_text(self.ITEM_TOTAL_LABEL)

    def get_tax(self) -> str:
        """Return tax label text, e.g. 'Tax: $3.20'."""
        return self.get_text(self.TAX_LABEL)

    def get_order_total(self) -> str:
        """Return total label text, e.g. 'Total: $43.19'."""
        return self.get_text(self.TOTAL_LABEL)

    def click_finish(self) -> None:
        """Click the Finish button to place the order."""
        self.logger.info("Clicking Finish to complete order")
        self.click(self.FINISH_BTN)

    # ── Step 3 queries ─────────────────────────────────────────────────────────

    def is_order_complete(self) -> bool:
        """True if the checkout-complete page header is visible."""
        return self.is_element_visible(self.COMPLETE_HEADER, timeout=5)

    def get_confirmation_header(self) -> str:
        """Return the large confirmation text, e.g. 'Thank you for your order!'."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_confirmation_text(self) -> str:
        """Return the sub-text beneath the confirmation header."""
        return self.get_text(self.COMPLETE_TEXT)

    def click_back_home(self) -> None:
        """Click 'Back Home' button on the completion page."""
        self.logger.info("Clicking Back Home")
        self.click(self.BACK_HOME_BTN)

    def is_pony_express_displayed(self) -> bool:
        """True if the success illustration image is visible."""
        return self.is_element_visible(self.PONY_EXPRESS_IMG, timeout=3)
