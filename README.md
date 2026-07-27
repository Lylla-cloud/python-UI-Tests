# AutomationExercise Python QA Framework

![Python Capstone](https://github.com/Lylla-cloud/python-UI-Tests/actions/workflows/python_capstone.yml/badge.svg)

A production-grade Python test automation framework for [AutomationExercise.com](https://automationexercise.com) — a full e-commerce platform. Built as a capstone project demonstrating senior QA engineering skills across UI automation, API testing, and BDD.

## What This Tests

| Layer | Coverage |
|---|---|
| UI (Selenium) | Login, logout, product search, browsing |
| API (Requests) | Products list, brands, search, user login verification |
| BDD (Behave) | Business-readable scenarios for all critical journeys |

## Tech Stack

- **Python 3.12** + **pip**
- **Selenium WebDriver 4** + **WebDriverManager** — browser automation
- **Requests** — API testing
- **Behave** — BDD test framework
- **Pytest** — Test runner and assertion framework
- **GitHub Actions** — CI/CD pipeline (API → UI → BDD)
- **Page Object Model** — maintainable UI framework

## Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── python_capstone.yml   # CI/CD configuration
├── features/                     # BDD Behave features and steps
│   └── steps/
├── pages/                        # Page Object Model components
│   ├── base_page.py
│   ├── home_page.py
│   ├── login_signup_page.py
│   └── products_page.py
├── test_data/                    # Static test data
├── tests/                        # UI and API test cases
│   ├── test_login.py
│   ├── test_products.py
│   ├── test_products_api.py
│   └── test_smoke.py
├── utils/                        # Shared utility modules
│   ├── config_reader.py
│   └── driver_manager.py
├── config.yaml                   # Environment and credential config
└── requirements.txt              # Project dependencies
```

## Getting Started

### Prerequisites

- Python 3.12 or newer installed.

### Installation

1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

- Run all Pytest tests:
  ```bash
  pytest -v
  ```
- Run a specific test suite (e.g., API tests):
  ```bash
  pytest tests/test_products_api.py -v
  ```
- Run Behave BDD tests:
  ```bash
  behave
  ```
