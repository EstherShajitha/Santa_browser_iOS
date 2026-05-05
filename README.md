# Santa iOS Enterprise Automation Framework

A production-ready end-to-end test automation framework for the Santa iOS browser. Built with pytest, Appium, and Page Object Model architecture.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Best Practices](#best-practices)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **Page Object Model (POM)** - Maintainable, reusable page object classes
- **Accessibility ID Locators** - Uses accessibility IDs to avoid fragile XPath selectors
- **Parallel Execution** - Run multiple tests concurrently with pytest-xdist
- **Automatic Screenshots** - Captures failure screenshots automatically
- **HTML Reporting** - Self-contained HTML reports with embedded logs and screenshots
- **Device Sharing** - Multiple parallel workers can share a single device safely
- **Real Device Support** - Optimized for real iOS devices and simulators
- **Analytics Capture** - Mitmproxy integration for network event monitoring
- **Comprehensive Logging** - Detailed logs for debugging and audit trails
- **CI/CD Ready** - GitHub Actions and Jenkins pipeline configurations included

---

## 📦 Prerequisites

### System Requirements

- **macOS** 11.0 or later (with Xcode installed)
- **Xcode Command Line Tools**
- **Xcode 13.0+** for simulator/device testing
- **Node.js 14+** (for Appium)
- **Python 3.10+**

### iOS Device Setup

- Real iOS device **14.0+** or iOS Simulator
- Device connected and recognized by Xcode
- **Developer Mode** enabled (for real devices)
- **Web Driver Agent** installed via Appium

### System Installation

```bash
# Install Homebrew (if needed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Install Appium
npm install -g appium

# Install Appium XCUITest Driver
appium driver install xcuitest

# Verify installation
appium --version
node --version
python3 --version
```

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-org/santa_ios_enterprise_framework.git
cd santa_ios_enterprise_framework
```

### 2. Create Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create `.env` file:

```bash
# Device Configuration
DEVICE_UDID_0=00008101-000541A91234C0AC
APPIUM_HOST=127.0.0.1
APPIUM_PORT=4723

# App Configuration
BUNDLE_ID=com.brave.ios
LOCALE=en_US
TIMEZONE=America/Los_Angeles

# Test Configuration
IMPLICIT_WAIT=10
EXPLICIT_WAIT=15
```

---

## 🎯 Quick Start

### Step 1: Start Appium Server

```bash
# Terminal 1
appium --port 4723
```

### Step 2: Run Tests

```bash
# Terminal 2
python -m pytest tests/ -v

# View report
open reports/report.html
```

---

## 🧪 Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/ntp/test_theme.py -v
```

### Run Specific Test
```bash
python -m pytest tests/ntp/test_theme.py::test_theme_changer -v
```

### Run with Parallel Execution
```bash
# Run with 2 parallel workers
python -m pytest tests/ -n 2 -v
```

### Run with Markers
```bash
# Run only smoke tests
python -m pytest -m smoke -v

# Run excluding skip markers
python -m pytest -m "not skip" -v
```

### Advanced Options

| Command | Description |
|---------|-------------|
| `-v` | Verbose output |
| `-s` | Show print statements |
| `-x` | Stop on first failure |
| `--lf` | Run last failed |
| `--ff` | Run failed first |
| `-k "pattern"` | Match test name pattern |
| `-m "marker"` | Run tests with marker |
| `-n NUM` | Parallel workers |

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── test.yml                 # GitHub Actions workflow
├── ci/
│   ├── Jenkinsfile              # Jenkins pipeline
│   └── JENKINS_SETUP.md         # Jenkins configuration guide
├── config/
│   ├── capabilities.py          # Appium iOS options
│   └── environment.py           # Environment config
├── locators/
│   ├── ntp_locators.py          # NTP page locators
│   ├── browser_locators.py      # Browser locators
│   ├── privacy_locators.py      # Privacy locators
│   └── settings_locators.py     # Settings locators
├── pages/
│   ├── base_page.py             # Base page object
│   ├── ntp_page.py              # NTP page object
│   ├── privacy_page.py          # Privacy page
│   ├── settings_page.py         # Settings page
│   └── browser_page.py          # Browser page
├── tests/
│   ├── ntp/
│   │   ├── test_theme.py        # Theme tests
│   │   └── test_tracker.py      # Tracker tests
│   ├── api/
│   │   └── test_endpoints.py    # API tests
│   └── privacy/
│       └── test_privacy.py      # Privacy tests
├── utils/
│   ├── logger.py                # Logging config
│   ├── waits.py                 # Wait helpers
│   ├── api_client.py            # HTTP client
│   └── analytics.py             # Analytics helpers
├── reports/
│   ├── report.html              # Generated HTML report
│   ├── junit.xml                # JUnit results
│   ├── screenshots/             # Failure screenshots
│   └── logs/                    # Test logs
├── conftest.py                  # Pytest fixtures
├── pytest.ini                   # Pytest config
├── Jenkinsfile                  # Jenkins pipeline
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── README.md                    # This file
```

---

## 🎨 Best Practices

### 1. Use Accessibility IDs for Locators

✅ **GOOD** - Accessibility ID (Maintainable)
```python
SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "NTPHomeFakeOmniboxAccessibilityID")
```

✅ **GOOD** - iOS Class Chain (Stable)
```python
SEARCH_FIELD = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeTextField")
```

❌ **AVOID** - XPath (Fragile)
```python
SEARCH_FIELD = (AppiumBy.XPATH, "//XCUIElementTypeTextField[@label='Search']")
```

### 2. Modular Page Objects

```python
class NTPPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_search_bar(self):
        element = self.wait_for_element(NTPLocators.SEARCH_BAR)
        element.click()
        
    def get_tracker_count(self):
        element = self.wait_for_element(NTPLocators.TRACKER_COUNT)
        return element.text
```

### 3. Reusable Test Code

```python
@pytest.mark.smoke
def test_theme_changer(driver):
    ntp_page = NTPPage(driver)
    ntp_page.click_theme_button()
    assert ntp_page.is_theme_changed()
```

### 4. Configuration-Driven Setup

Use `.env` file for all configuration instead of hardcoding values:

```python
from dotenv import load_dotenv
import os

load_dotenv()
DEVICE_UDID = os.getenv("DEVICE_UDID_0")
APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")
```

### 5. Separate Test Data

```python
# tests/data/test_data.py
TEST_URLS = {
    "google": "https://www.google.com",
    "wikipedia": "https://www.wikipedia.org"
}
```

### 6. Proper Logging

```python
from utils.logger import get_logger

logger = get_logger()

def test_example(driver):
    logger.info("Test started")
    logger.debug("Debug info")
    logger.error("Error occurred")
```

---

## 🔄 CI/CD Integration

### GitHub Actions

Automatic testing on push/PR:

```bash
# Workflow file: .github/workflows/test.yml
# Features:
# - Runs on Python 3.10, 3.11, 3.12
# - Parallel test execution
# - HTML report generation
# - Screenshot preservation
# - Artifact archiving
```

**Setup:**
1. Push code to GitHub
2. Workflow automatically triggers
3. View results in Actions tab
4. Download artifacts (reports, screenshots)

### Jenkins Pipeline

Parameterized CI/CD pipeline:

```bash
# Pipeline file: Jenkinsfile
# Features:
# - Build parameters (test suite, workers)
# - HTML report publishing
# - Artifact archiving
# - Email notifications (optional)
```

**Setup Steps:**
1. See `ci/JENKINS_SETUP.md` for detailed instructions
2. Create new Pipeline job
3. Point to `Jenkinsfile`
4. Configure agent with label: `macos`
5. Set up webhooks for auto-trigger

---

## 🔧 Configuration Files

### pytest.ini

```ini
[pytest]
pythonpath = .
addopts = -v --tb=short --html=reports/report.html --self-contained-html
testpaths = tests
markers =
    smoke: Critical tests
    regression: Full regression
```

### requirements.txt

Contains all dependencies with versions:
- pytest and plugins
- Appium Python Client
- Selenium
- mitmproxy (analytics)
- xlsxwriter (reports)

---

## 📊 Viewing Reports

### HTML Report
```bash
# Auto-generated after every test run
open reports/report.html
```

**Contains:**
- Test summary
- Detailed results
- Embedded screenshots
- Attached logs
- Environment info

### Logs
```bash
# View test logs
tail -f reports/logs/test.log

# Search for errors
grep "ERROR" reports/logs/test.log
```

---

## 🐛 Troubleshooting

### Appium Connection Error

```bash
# Check port is available
lsof -i :4723

# Kill process on port
kill -9 <PID>

# Start Appium on different port
appium --port 4724
```

### Device Not Found

```bash
# List devices
xcrun simctl list devices

# Check Xcode setup
sudo xcode-select --reset
sudo xcode-select --install
```

### Test Timeout

Edit `pytest.ini`:
```ini
timeout = 600
```

### Virtual Environment Issues

```bash
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 📚 Resources

- [Appium Docs](https://appium.io/docs/)
- [pytest Docs](https://docs.pytest.org/)
- [Selenium Docs](https://selenium.dev/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [Jenkins](https://www.jenkins.io/)