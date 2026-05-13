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
import os
import stat
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
    def _resolve_driver_executable(driver_path: str, expected_name: str) -> str:
        """Resolve the actual driver binary from webdriver-manager output."""
        def ensure_executable(path: str) -> None:
            if os.path.isfile(path):
                current_mode = os.stat(path).st_mode
                if not (current_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)):
                    os.chmod(path, current_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

        if os.path.isfile(driver_path) and os.path.basename(driver_path).lower() == expected_name.lower():
            ensure_executable(driver_path)
            return driver_path

        lookup_dir = driver_path if os.path.isdir(driver_path) else os.path.dirname(driver_path)
        candidate = os.path.join(lookup_dir, expected_name)
        if os.path.isfile(candidate):
            ensure_executable(candidate)
            return candidate

        raise RuntimeError(
            f"Could not resolve executable '{expected_name}' from webdriver-manager path: {driver_path}"
        )

    @staticmethod
    def _chrome(headless: bool) -> webdriver.Chrome:
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")          # suppress console noise
        if headless:
            options.add_argument("--headless=new")     # new headless (Chrome 112+)
            options.add_argument(f"--window-size={DriverFactory._HEADLESS_WINDOW}")
        driver_path = ChromeDriverManager().install()
        driver_path = DriverFactory._resolve_driver_executable(driver_path, "chromedriver")
        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)

    @staticmethod
    def _firefox(headless: bool) -> webdriver.Firefox:
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
            options.add_argument(f"--width={DriverFactory._HEADLESS_WINDOW.split(',')[0]}")
            options.add_argument(f"--height={DriverFactory._HEADLESS_WINDOW.split(',')[1]}")
        driver_path = GeckoDriverManager().install()
        driver_path = DriverFactory._resolve_driver_executable(driver_path, "geckodriver")
        service = FirefoxService(driver_path)
        return webdriver.Firefox(service=service, options=options)

    @staticmethod
    def _edge(headless: bool) -> webdriver.Edge:
        options = EdgeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument(f"--window-size={DriverFactory._HEADLESS_WINDOW}")
        driver_path = EdgeChromiumDriverManager().install()
        driver_path = DriverFactory._resolve_driver_executable(driver_path, "msedgedriver")
        service = EdgeService(driver_path)
        return webdriver.Edge(service=service, options=options)
