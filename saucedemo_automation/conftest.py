"""
conftest.py
───────────
Shared pytest fixtures available to every test module.

Key fixtures
------------
driver      – yields a configured WebDriver instance; tears down after the test.
logged_in   – yields a driver that is already on the inventory page.

Command-line options (added via pytest_addoption)
-------------------------------------------------
--browser   chrome | firefox | edge          (default: chrome)
--headless  run the browser in headless mode  (flag, default: False)
--base-url  override the target URL           (default: https://www.saucedemo.com)
"""

import pytest
from utils.driver_factory import DriverFactory
from utils.screenshot_helper import ScreenshotHelper
from pages.login_page import LoginPage
import logging

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────────────────────────────────────
#  CLI options
# ──────────────────────────────────────────────────────────────────────────────

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--browser",   action="store", default="chrome",
                     help="Browser to run tests: chrome | firefox | edge")
    parser.addoption("--headless",  action="store_true", default=False,
                     help="Run browser in headless mode")
    parser.addoption("--base-url",  action="store", default="https://www.saucedemo.com",
                     help="Base URL of the application under test")


# ──────────────────────────────────────────────────────────────────────────────
#  HTML-report enhancements
# ──────────────────────────────────────────────────────────────────────────────

def pytest_configure(config: pytest.Config) -> None:
    """Attach project metadata to the HTML report header."""
    config._metadata = {          # type: ignore[attr-defined]
        "Project":  "SauceDemo Automation Suite",
        "Tester":   "QA Automation Framework",
        "Browser":  config.getoption("--browser", default="chrome"),
        "Headless": config.getoption("--headless", default=False),
    }


# ──────────────────────────────────────────────────────────────────────────────
#  Core driver fixture
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest):
    """
    Provide a fresh WebDriver for each test function.
    Screenshots are captured automatically on failure.
    """
    browser   = request.config.getoption("--browser")
    headless  = request.config.getoption("--headless")
    base_url  = request.config.getoption("--base-url")

    logger.info("Launching %s (headless=%s)", browser, headless)
    web_driver = DriverFactory.get_driver(browser=browser, headless=headless)
    web_driver.get(base_url)

    yield web_driver

    # ── Teardown ──────────────────────────────────────────────────────────────
    # Capture a screenshot if the test failed
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        ScreenshotHelper.capture(web_driver, request.node.name)
        logger.warning("Test FAILED – screenshot saved for: %s", request.node.name)

    logger.info("Closing browser after: %s", request.node.name)
    web_driver.quit()


# ──────────────────────────────────────────────────────────────────────────────
#  Hook: mark test outcome so the driver fixture can read it
# ──────────────────────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach phase reports to the test node so fixtures can inspect them."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


# ──────────────────────────────────────────────────────────────────────────────
#  Convenience: pre-logged-in driver
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def logged_in(driver):
    """
    Yield a driver that has already completed a successful login.
    Tests that don't need to exercise the login page should use this fixture.
    """
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    yield driver
