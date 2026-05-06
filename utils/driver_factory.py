"""
utils/driver_factory.py
────────────────────────
Factory that creates a Selenium WebDriver instance for the requested browser.

Supported browsers : chrome | firefox | edge
Headless mode      : pass headless=True (works for all three browsers)
Driver management  : webdriver-manager handles binary downloads automatically,
                     so no manual chromedriver/geckodriver installation is needed.
"""

import logging
from selenium import webdriver
from selenium.webdriver.chrome.service   import Service as ChromeService
from selenium.webdriver.firefox.service  import Service as FirefoxService
from selenium.webdriver.edge.service     import Service as EdgeService
from selenium.webdriver.chrome.options   import Options as ChromeOptions
from selenium.webdriver.firefox.options  import Options as FirefoxOptions
from selenium.webdriver.edge.options     import Options as EdgeOptions
from webdriver_manager.chrome   import ChromeDriverManager
from webdriver_manager.firefox  import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

logger = logging.getLogger(__name__)


class DriverFactory:
    """Static factory – call DriverFactory.get_driver(browser, headless)."""

    # Window size used in headless mode (prevents layout issues)
    _HEADLESS_WINDOW = "1920,1080"

    @staticmethod
    def get_driver(browser: str = "chrome", headless: bool = False) -> webdriver.Remote:
        """
        Create and return a configured WebDriver.

        Parameters
        ----------
        browser  : 'chrome' | 'firefox' | 'edge'  (case-insensitive)
        headless : run without a visible browser window

        Returns
        -------
        WebDriver instance with implicit wait disabled
        (explicit waits are used throughout the framework).
        """
        browser = browser.lower().strip()
        logger.info("Creating %s driver  (headless=%s)", browser, headless)

        if browser == "chrome":
            driver = DriverFactory._chrome(headless)
        elif browser == "firefox":
            driver = DriverFactory._firefox(headless)
        elif browser == "edge":
            driver = DriverFactory._edge(headless)
        else:
            raise ValueError(
                f"Unsupported browser: '{browser}'. Choose chrome | firefox | edge."
            )

        # Global settings
        driver.maximize_window()
        driver.implicitly_wait(0)   # rely on explicit waits only
        return driver

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    
    def _chrome(headless: bool) -> webdriver.Chrome:
        options = ChromeOptions()

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")

        # ✅ IMPORTANT FIX FOR FEDORA / LINUX
        options.binary_location = "/usr/bin/google-chrome"

        if headless:
            options.add_argument("--headless=new")
            options.add_argument(f"--window-size={DriverFactory._HEADLESS_WINDOW}")

        service = ChromeService(ChromeDriverManager().install())

        return webdriver.Chrome(service=service, options=options)
    @staticmethod
    def _edge(headless: bool) -> webdriver.Edge:
        options = EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument(f"--window-size={DriverFactory._HEADLESS_WINDOW}")
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
