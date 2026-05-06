#  SauceDemo Selenium Automation Framework

A professional, production-grade test automation framework for the [SauceDemo](https://www.saucedemo.com/) demo e-commerce website, built with **Python**, **Selenium WebDriver**, **PyTest**, and the **Page Object Model (POM)** design pattern.

---

## Table of Contents

- [Project Overview](#-project-overview)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Test Coverage](#-test-coverage)
- [Installation](#-installation)
- [Running Tests](#-running-tests)
- [Generating Reports](#-generating-reports)
- [Screenshots on Failure](#-screenshots-on-failure)
- [Advanced Options](#-advanced-options)
- [Best Practices Applied](#-best-practices-applied)

---

## Project Overview

This framework automates end-to-end testing of the SauceDemo e-commerce website, covering:

| Area        | Scenarios |
|-------------|-----------|
| Login       | Valid/invalid credentials, empty fields, locked user, logout |
| Products    | List verification, add/remove items, cart badge, sorting |
| Cart        | Open cart, verify items, remove items, continue shopping |
| Checkout    | Form validation, full order flow, confirmation page |

**Total test cases: 40**

---

## Technologies Used

| Tool / Library        | Version   | Purpose                          |
|-----------------------|-----------|----------------------------------|
| Python                | 3.10+     | Programming language             |
| Selenium WebDriver    | 4.18.1    | Browser automation               |
| PyTest                | 8.1.1     | Test runner & assertion library  |
| pytest-html           | 4.1.1     | HTML test reports                |
| pytest-xdist          | 3.5.0     | Parallel test execution          |
| webdriver-manager     | 4.0.1     | Auto-download browser drivers    |
| pytest-timeout        | 2.3.1     | Per-test timeout guard           |
| Pillow                | 10.2.0    | Screenshot support               |

---

## Project Structure

```
saucedemo_automation/
│
├── tests/                    # Test modules
│   ├── __init__.py
│   ├── test_login.py         # 10 login test cases
│   ├── test_products.py      # 11 product test cases
│   ├── test_cart.py          # 10 cart test cases
│   └── test_checkout.py      # 15 checkout test cases
│
├── pages/                    # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py          # Abstract base with shared helpers
│   ├── login_page.py         # Login page interactions
│   ├── inventory_page.py     # Products / inventory interactions
│   ├── cart_page.py          # Cart page interactions
│   └── checkout_page.py      # Checkout steps 1-3 interactions
│
├── utils/                    # Framework utilities
│   ├── __init__.py
│   ├── driver_factory.py     # WebDriver creation (Chrome/Firefox/Edge)
│   ├── screenshot_helper.py  # Auto-screenshot on failure
│   └── logger.py             # Rotating file + console logging
│
├── screenshots/              # Auto-created; failure screenshots saved here
├── reports/                  # Auto-created; HTML report saved here
├── logs/                     # Auto-created; rotating log file saved here
│
├── conftest.py               # Shared pytest fixtures & CLI options
├── pytest.ini                # PyTest configuration & markers
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

---

## Test Coverage

### Login Tests (`test_login.py`)
| ID     | Test Case                          | Marker        |
|--------|------------------------------------|---------------|
| TC_L01 | Valid login                        | smoke, login  |
| TC_L02 | Invalid password                   | regression    |
| TC_L03 | Invalid username                   | regression    |
| TC_L04 | Empty username field               | regression    |
| TC_L05 | Empty password field               | regression    |
| TC_L06 | Both fields empty                  | regression    |
| TC_L07 | Locked-out user                    | regression    |
| TC_L08 | Dismiss error banner               | regression    |
| TC_L09 | Logout via side menu               | smoke, login  |
| TC_L10 | Page title verification            | smoke, login  |

### Product Tests (`test_products.py`)
| ID     | Test Case                          | Marker          |
|--------|------------------------------------|-----------------|
| TC_P01 | Product list loads (6 items)       | smoke, products |
| TC_P02 | Page title is "Products"           | smoke           |
| TC_P03 | Add single product to cart         | smoke           |
| TC_P04 | Badge increments per product       | regression      |
| TC_P05 | Add multiple products              | regression      |
| TC_P06 | Remove product from inventory page | regression      |
| TC_P07 | Badge disappears when cart empty   | regression      |
| TC_P08 | Sort A→Z                           | regression      |
| TC_P09 | Sort Z→A                           | regression      |
| TC_P10 | Sort low → high price              | regression      |
| TC_P11 | Sort high → low price              | regression      |

### Cart Tests (`test_cart.py`)
| ID     | Test Case                          | Marker      |
|--------|------------------------------------|-------------|
| TC_C01 | Cart page title "Your Cart"        | smoke, cart |
| TC_C02 | Cart URL is /cart.html             | smoke       |
| TC_C03 | Added product appears in cart      | smoke       |
| TC_C04 | Multiple products in cart          | regression  |
| TC_C05 | Item quantity defaults to 1        | regression  |
| TC_C06 | Remove item from cart page         | regression  |
| TC_C07 | Cart empty after removing all      | regression  |
| TC_C08 | Continue Shopping → inventory      | regression  |
| TC_C09 | Checkout button → step 1           | smoke       |
| TC_C10 | Cart icon opens cart               | smoke       |

### Checkout Tests (`test_checkout.py`)
| ID      | Test Case                          | Marker          |
|---------|------------------------------------|-----------------|
| TC_CH01 | Step-1 URL correct                 | smoke, checkout |
| TC_CH02 | Cancel on step-1 → cart            | regression      |
| TC_CH03 | Empty first name error             | regression      |
| TC_CH04 | Empty last name error              | regression      |
| TC_CH05 | Empty zip code error               | regression      |
| TC_CH06 | All fields empty error             | regression      |
| TC_CH07 | Valid info → step-2                | smoke           |
| TC_CH08 | Step-2 lists ordered products      | regression      |
| TC_CH09 | Step-2 shows price summary         | regression      |
| TC_CH10 | Cancel on step-2 → inventory      | regression      |
| TC_CH11 | Finish completes order             | smoke           |
| TC_CH12 | Completion shows thank-you header  | smoke           |
| TC_CH13 | Completion shows success image     | regression      |
| TC_CH14 | Back Home → inventory              | regression      |
| TC_CH15 | Full end-to-end purchase flow      | smoke           |

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Google Chrome (recommended) / Firefox / Microsoft Edge
- Git (to clone the repository)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ghanemhassan/SauceDemo_Selenium_Automation_Framework_V1.git
cd saucedemo_automation

# 2. Create and activate a virtual environment (recommended)
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS / Linux
source venv/bin/activate

# 3. Install all dependencies
pip install -r requirements.txt
```

> **Note:** `webdriver-manager` will automatically download the correct browser driver. No manual chromedriver installation is needed.

---

## Running Tests

### Run all tests
```bash
pytest
```

### Run a specific test file
```bash
pytest tests/test_login.py
pytest tests/test_products.py
pytest tests/test_cart.py
pytest tests/test_checkout.py
```

### Run a specific test case
```bash
pytest tests/test_login.py::TestLogin::test_valid_login
```

### Run tests by marker
```bash
# Smoke tests only (fast, critical paths)
pytest -m smoke

# Regression suite
pytest -m regression

# All login tests
pytest -m login

# All cart tests
pytest -m cart
```

### Run in verbose mode (see test names)
```bash
pytest -v
```

### Run with print output visible
```bash
pytest -s
```

---

## Generating Reports

An HTML report is generated automatically after every test run:

```
reports/report.html
```

To open after running:
```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html

# Windows
start reports/report.html
```

The report includes:
- Test results (pass / fail / skip)
- Duration per test
- Error messages and tracebacks
- Environment metadata (browser, headless mode)

---

## Screenshots on Failure

Screenshots are **automatically captured** whenever a test fails and saved to:

```
screenshots/<test_name>_<timestamp>.png
```

Example:
```
screenshots/test_valid_login_20240315_143022.png
```

---

## Advanced Options

### Headless Mode (no visible browser)
```bash
pytest --headless
```

### Different Browsers
```bash
# Chrome (default)
pytest --browser=chrome

# Firefox
pytest --browser=firefox

# Microsoft Edge
pytest --browser=edge
```

### Override Base URL
```bash
pytest --base-url=https://www.saucedemo.com
```

### Parallel Execution (faster runs with pytest-xdist)
```bash
# Run with 4 parallel workers
pytest -n 4

# Automatic (uses all available CPU cores)
pytest -n auto
```

### Combine Options
```bash
# Headless Chrome, smoke tests only, 2 parallel workers
pytest --headless --browser=chrome -m smoke -n 2
```

### Set Test Timeout
```bash
pytest --timeout=60
```

---

## Best Practices Applied

| Practice                   | Implementation                                     |
|----------------------------|----------------------------------------------------|
| Page Object Model          | Each page has its own class with locators + methods|
| Explicit Waits             | `WebDriverWait` used throughout; no `sleep()`      |
| DRY (Don't Repeat Yourself)| Shared `BasePage` and `conftest.py` fixtures       |
| Logging                    | Rotating file + console logging per module         |
| Screenshot on Failure      | Auto-captured via `pytest_runtest_makereport` hook |
| Headless Support           | `--headless` CLI flag for all three browsers       |
| Cross-browser Support      | Chrome, Firefox, Edge via `--browser` flag         |
| Parallel Execution         | `pytest-xdist` with `-n` flag                      |
| Markers                    | `smoke`, `regression`, `login`, `products`, etc.   |
| Timeout Guard              | `pytest-timeout` prevents hanging tests            |
| Auto Driver Management     | `webdriver-manager` downloads correct driver       |
| Clean Teardown             | `driver.quit()` always called in fixture teardown  |

---

## Test Credentials

| Username        | Password      | Status       |
|-----------------|---------------|--------------|
| standard_user   | secret_sauce  |    Valid     |
| locked_out_user | secret_sauce  |    Locked    |
| problem_user    | secret_sauce  |    Buggy UI  |

---

##  License

This project is intended for educational and demonstration purposes.
