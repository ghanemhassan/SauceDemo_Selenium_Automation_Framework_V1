"""
utils/screenshot_helper.py
───────────────────────────
Utility for capturing and saving browser screenshots.

Screenshots are saved to the /screenshots/ directory with a timestamped
filename so each failure produces a unique, traceable file.
"""

import os
import logging
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)

# Absolute path to the screenshots folder (relative to project root)
SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "screenshots"
)


class ScreenshotHelper:
    """Static helper – call ScreenshotHelper.capture(driver, test_name)."""

    @staticmethod
    def capture(driver: WebDriver, test_name: str) -> str:
        """
        Take a full-page screenshot and save it to /screenshots/.

        Parameters
        ----------
        driver    : active WebDriver instance
        test_name : used as part of the filename (spaces replaced with '_')

        Returns
        -------
        Absolute file path of the saved screenshot (empty string on error).
        """
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

        # Build a unique, human-readable filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = test_name.replace(" ", "_").replace("/", "_")
        filename  = f"{safe_name}_{timestamp}.png"
        filepath  = os.path.join(SCREENSHOTS_DIR, filename)

        try:
            driver.save_screenshot(filepath)
            logger.info("Screenshot saved: %s", filepath)
            return filepath
        except Exception as exc:
            logger.error("Failed to capture screenshot: %s", exc)
            return ""

    @staticmethod
    def capture_element(driver: WebDriver, element, test_name: str) -> str:
        """
        Take a screenshot of a specific WebElement.

        Parameters
        ----------
        driver    : active WebDriver instance
        element   : WebElement to screenshot
        test_name : base name for the file

        Returns
        -------
        Absolute file path of the saved screenshot (empty string on error).
        """
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = test_name.replace(" ", "_")
        filename  = f"{safe_name}_element_{timestamp}.png"
        filepath  = os.path.join(SCREENSHOTS_DIR, filename)

        try:
            element.screenshot(filepath)
            logger.info("Element screenshot saved: %s", filepath)
            return filepath
        except Exception as exc:
            logger.error("Failed to capture element screenshot: %s", exc)
            return ""
