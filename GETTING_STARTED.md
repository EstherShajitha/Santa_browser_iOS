# Getting Started Guide

Quick reference for setting up and running the Santa iOS Enterprise Framework.

## ⚡ 5-Minute Setup

### 1. Install System Dependencies

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js
brew install node

# Install Appium
npm install -g appium
appium driver install xcuitest

# Verify
appium --version  # Should show 2.0+
node --version    # Should show 14+
```

### 2. Clone and Setup

```bash
# Clone repository
git clone https://github.com/your-org/santa_ios_enterprise_framework.git
cd santa_ios_enterprise_framework

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Device

```bash
# Find your device UDID
xcrun simctl list devices

# Copy .env.example to .env
cp .env.example .env

# Edit .env and set DEVICE_UDID_0
nano .env  # Or use your preferred editor
```

### 4. Start Testing

```bash
# Terminal 1: Start Appium
appium --port 4723

# Terminal 2: Run tests
python -m pytest tests/ -v

# Open report
open reports/report.html
```

---

## 📋 Common Commands

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/ntp/test_theme.py -v

# Specific test
pytest tests/ntp/test_theme.py::test_theme_changer -v

# With parallel execution
pytest tests/ -n 2 -v

# Only smoke tests
pytest -m smoke -v
```

### Viewing Results

```bash
# Open HTML report
open reports/report.html

# View logs
tail -f reports/logs/test.log

# Check screenshots
ls -la reports/screenshots/
```

### Device Management

```bash
# List devices
xcrun simctl list devices

# Erase simulator
xcrun simctl erase <device-id>

# Boot simulator
xcrun simctl boot <device-id>
```

### Troubleshooting

```bash
# Kill Appium
pkill -f appium

# Check port
lsof -i :4723

# Clear venv
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Reset Xcode
sudo xcode-select --reset
```

---

## 🎯 First Test Walkthrough

### 1. Understand the Page Object

```python
# pages/ntp_page.py
class NTPPage(BasePage):
    def click_search_bar(self):
        """Click search bar"""
        element = self.wait_for_element(NTPLocators.SEARCH_BAR)
        element.click()
```

### 2. Write Your Test

```python
# tests/ntp/test_example.py
import pytest
from pages.ntp_page import NTPPage
from utils.logger import get_logger

logger = get_logger()

@pytest.mark.smoke
def test_search_bar_clickable(driver):
    """Test that search bar is clickable"""
    # Arrange
    ntp_page = NTPPage(driver)
    
    # Act
    logger.info("Clicking search bar")
    ntp_page.click_search_bar()
    
    # Assert
    assert ntp_page.is_search_active(), "Search bar should be active"
    logger.info("Test passed: Search bar is clickable")
```

### 3. Run Your Test

```bash
pytest tests/ntp/test_example.py::test_search_bar_clickable -v -s
```

### 4. Check Results

```bash
open reports/report.html
```

---

## 📊 CI/CD Quick Start

### GitHub Actions

1. Push code to GitHub
2. Workflow automatically runs
3. Check Actions tab for results
4. Download artifacts (reports, screenshots)

### Jenkins

1. Create Pipeline job
2. Point to `Jenkinsfile`
3. Configure agent: `macos`
4. Run build with parameters
5. View "pytest HTML Report"

---

## 📚 Important Files

| File | Purpose |
|------|---------|
| `conftest.py` | Pytest fixtures and Appium setup |
| `pytest.ini` | Pytest configuration |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables |
| `README.md` | Full documentation |
| `.github/workflows/test.yml` | GitHub Actions workflow |
| `Jenkinsfile` | Jenkins pipeline |

---

## ✅ Checklist

Before starting:
- [ ] Python 3.10+ installed
- [ ] Xcode installed
- [ ] Node.js and npm installed
- [ ] Appium installed (`appium --version`)
- [ ] iOS device/simulator connected
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Appium server running on port 4723

---

## 🆘 Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| `Connection refused` | Start Appium: `appium --port 4723` |
| `Device not found` | Run: `xcrun simctl list devices` |
| `Module not found` | Reinstall: `pip install -r requirements.txt` |
| `Permission denied` | Reset Xcode: `sudo xcode-select --reset` |
| `Port 4723 in use` | Kill process: `lsof -i :4723` and `kill -9 <PID>` |
| `Timeout errors` | Increase timeout in `pytest.ini` |

---

## 🔗 Helpful Links

- [Appium Documentation](https://appium.io/docs/)
- [pytest Guide](https://docs.pytest.org/)
- [Selenium WebDriver](https://www.selenium.dev/)
- [iOS Automation](https://developer.apple.com/documentation/xctest)

---

## 💡 Pro Tips

1. **Use markers for test organization:**
   ```python
   @pytest.mark.smoke
   @pytest.mark.regression
   def test_feature(driver):
       pass
   ```

2. **Use `-x` to stop at first failure:**
   ```bash
   pytest -x tests/
   ```

3. **Use `-k` to run tests by name pattern:**
   ```bash
   pytest -k "search" -v
   ```

4. **Use `-v -s` for verbose output with prints:**
   ```bash
   pytest -v -s tests/
   ```

5. **Check logs while tests run:**
   ```bash
   tail -f reports/logs/test.log
   ```

6. **Use `--lf` to run last failed tests:**
   ```bash
   pytest --lf -v
   ```

7. **Parallel execution speeds up testing:**
   ```bash
   pytest -n 2 tests/
   ```

---

## 📞 Need Help?

1. Check the full [README.md](../README.md)
2. Read [HTML_REPORTING.md](../HTML_REPORTING.md)
3. Review [CI_CD_BEST_PRACTICES.md](CI_CD_BEST_PRACTICES.md)
4. Check test logs: `tail -f reports/logs/test.log`
5. Review Appium logs in terminal

---

**Happy Testing! 🚀**
