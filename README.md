# Reno — Python Selenium Website Testing Framework

A modular, high-performance website automation and quality testing application built with **Python 3**, **Selenium WebDriver**, **Pytest**, and **Flask**.

---

## Features

- **Page Object Model (POM)**: Clean abstraction layer (`pages/base_page.py`, `pages/generic_page.py`).
- **Multi-Browser Driver Manager**: Supports Google Chrome and Mozilla Firefox with Headless and Headed modes via `webdriver-manager`.
- **Automated Quality Suites**:
  - ⚡ **Smoke & Availability**: Checks reachability, page titles, HTML meta tags, and screenshots.
  - 🔗 **Link Crawler**: Scrapes links, checks broken HTTP status codes (404/500), and records response times.
  - 📝 **Form Field Audit**: Inspects forms, text inputs, and interactivity.
  - 📊 **Performance & Accessibility**: Validates heading tags (`h1`/`h2`), image `alt` text, and page load render speed.
- **Dual Execution Interfaces**:
  - **CLI Runner**: `python runner.py` with custom arguments (`--url`, `--browser`, `--headless`).
  - **Web Dashboard**: Interactive Flask app (`python app.py`) with real-time logs, progress tracking, and screenshot modal previews.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run via CLI

Run test suite against any website:

```bash
python runner.py --url https://example.com --browser chrome --headless
```

To run using pytest directly:

```bash
pytest --target-url=https://example.com --browser=chrome --headless
```

### 3. Launch Web Dashboard UI

Start the Flask server:

```bash
python app.py
```

Then open your browser and visit **`http://localhost:5000`**.
