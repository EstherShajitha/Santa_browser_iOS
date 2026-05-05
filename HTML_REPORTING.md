# HTML Reporting Implementation

## Overview

The Santa iOS Enterprise Framework now uses **pytest-html** for generating self-contained HTML reports with embedded screenshots, logs, and test results.

## Features

✅ **Test Summary** - Overview of passed, failed, and error tests  
✅ **Pass/Fail Status** - Detailed results for each test  
✅ **Screenshots Embedded** - Failure screenshots captured automatically  
✅ **Logs Attached** - Complete test execution logs included  
✅ **Self-Contained** - Single HTML file with all assets embedded  
✅ **No External Dependencies** - No server required to view reports  

## Setup

### Dependencies

The framework automatically includes `pytest-html` in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Configuration

The `pytest.ini` file is configured to automatically generate HTML reports:

```ini
[pytest]
pythonpath = .
addopts = -v --tb=short --html=reports/report.html --self-contained-html
testpaths = tests
```

Key options:
- `--html=reports/report.html` - Output report path
- `--self-contained-html` - Embeds all CSS/JS/media into single file

## Running Tests

### Standard Test Run

```bash
python -m pytest -v
```

This automatically:
1. Executes all tests in the `tests/` directory
2. Captures failures with screenshots
3. Collects logs from `reports/logs/test.log`
4. Generates HTML report at `reports/report.html`

### Run Specific Tests

```bash
python -m pytest tests/ntp/test_theme.py -v
```

### Run with Parallel Execution

```bash
python -m pytest -n 2 -v
```

The framework includes worker-safe locking so parallel workers can share a single device.

## Viewing Reports

After running tests, open the generated report in your browser:

```bash
# macOS
open reports/report.html

# Linux
xdg-open reports/report.html

# Windows
start reports/report.html
```

The HTML report includes:

- **Summary Section** - Total passed/failed/error counts
- **Results Table** - Detailed results for each test
- **Expandable Rows** - Click test rows to see detailed output
- **Screenshots** - Embedded PNG images from test failures
- **Logs** - Complete test execution logs
- **Environment Info** - Python version, platform, plugins used

## Report Structure

```
reports/
├── report.html              # Main HTML report (self-contained)
├── screenshots/             # Test failure screenshots
│   ├── test_theme_changer_setup.png
│   ├── test_theme_changer_call.png
│   └── test_theme_changer_teardown.png
└── logs/
    └── test.log            # Test execution logs
```

## Screenshot Capture

Screenshots are automatically captured when:

1. **Setup Phase Fails** - Error during fixture initialization
2. **Test Execution Fails** - Assertion or runtime error
3. **Teardown Phase Fails** - Error during cleanup

The screenshot filename format: `{test_name}_{phase}.png`

Example:
- `test_theme_changer_setup.png` - Setup phase failure
- `test_theme_changer_call.png` - Test execution failure
- `test_theme_changer_teardown.png` - Teardown failure

## Log Attachment

The test log file (`reports/logs/test.log`) is automatically attached to failure reports. This includes:

- Test execution start/stop timestamps
- Driver initialization logs
- Custom logging from your tests
- Error stack traces
- Connection warnings and retries

## Customization

### Add Custom Logging

In your tests, use the logger to add custom information:

```python
from utils.logger import get_logger

logger = get_logger()

def test_example(driver):
    logger.info("Starting test execution")
    logger.info("Navigating to home page")
    # ... your test code ...
    logger.info("Test completed successfully")
```

### Modify Screenshot Capture

Edit the `pytest_runtest_makereport` hook in `conftest.py`:

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Customize screenshot capture logic here
```

### Change Report Output Path

Edit `pytest.ini`:

```ini
addopts = -v --tb=short --html=path/to/custom/report.html --self-contained-html
```

## Report Structure (HTML)

The generated HTML report contains:

- **Environment Section** - Python version, platform, installed plugins
- **Summary Statistics** - Test counts, execution time
- **Test Details** - Individual test results with collapsible rows
- **Failure Information** - Error messages, logs, and screenshots
- **Media Section** - Embedded screenshots with navigation
- **Log Viewer** - Expandable log section with scroll control

## Benefits

1. **No External Dependencies** - No Allure server, no complex setup
2. **Portable** - Single HTML file can be emailed or shared
3. **Fast** - Generates in seconds, minimal overhead
4. **Comprehensive** - Screenshots and logs embedded automatically
5. **Browser-Compatible** - Works in any modern browser
6. **CI/CD Ready** - Perfect for artifact storage in pipelines

## Comparison with Previous Setup

| Feature | Previous (Allure) | Current (pytest-html) |
|---------|-------------------|----------------------|
| Server Required | Yes | No |
| Portable | No | Yes |
| Setup Complexity | High | Low |
| Embedded Assets | No | Yes |
| Screenshots | Manual | Automatic |
| Logs | Separate | Embedded |

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Run Tests
  run: python -m pytest -v

- name: Upload Report
  if: always()
  uses: actions/upload-artifact@v3
  with:
    name: test-report
    path: reports/report.html
```

### Jenkins Example

```groovy
stage('Generate Report') {
    steps {
        sh 'python -m pytest -v'
        archiveArtifacts artifacts: 'reports/report.html'
    }
}
```

## Troubleshooting

### Report Not Generated

- Verify `pytest-html` is installed: `pip list | grep pytest-html`
- Check `pytest.ini` has correct `--html` path
- Ensure `reports/` directory exists

### Screenshots Not Appearing

- Verify driver is properly initialized
- Check `reports/screenshots/` directory exists
- Ensure test runs long enough to capture screenshot
- Verify Appium server is running (if using mobile automation)

### Logs Not Attached

- Check `reports/logs/test.log` exists
- Verify logger is initialized: `from utils.logger import get_logger`
- Ensure log file has write permissions

### Report File Too Large

- Clear old `reports/screenshots/` directory
- Run with fewer parallel workers
- Consider archiving older reports

## Additional Resources

- [pytest-html Documentation](https://pytest-html.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Appium Documentation](https://appium.io/)
