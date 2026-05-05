# CI/CD Best Practices Guide

This document outlines best practices for running the Santa iOS Enterprise Framework in CI/CD environments.

## Table of Contents

- [GitHub Actions](#github-actions)
- [Jenkins](#jenkins)
- [General Best Practices](#general-best-practices)
- [Troubleshooting](#troubleshooting)

---

## GitHub Actions

### Overview

The framework includes a complete GitHub Actions workflow at `.github/workflows/test.yml` that automatically runs tests on:
- Push to `main` or `develop` branches
- Pull requests
- Daily schedule (2 AM UTC)

### Features

- **Multi-version Testing**: Python 3.10, 3.11, 3.12
- **Parallel Execution**: Concurrent test workers
- **Artifact Storage**: 30-day retention
- **Report Publishing**: HTML reports with test results
- **Screenshot Preservation**: Failure screenshots archived

### Trigger Conditions

**Automatic Triggers:**
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC
```

### Workflow Steps

1. **Checkout Code** - Fetch repository
2. **Setup Python** - Install specified Python version
3. **Install Dependencies** - System & Python packages
4. **Verify Tools** - Check Node.js, Appium, etc.
5. **Start Appium** - Launch Appium server
6. **Create Reports Directory** - Prepare output folders
7. **Run Tests** - Execute pytest
8. **Generate Reports** - Create HTML and JUnit reports
9. **Upload Artifacts** - Archive reports, screenshots, logs
10. **Publish Results** - Parse and display test results

### View Results

**In GitHub UI:**
1. Go to repo → Actions tab
2. Select workflow run
3. Check "Summary" for results
4. Download artifacts:
   - `test-report-*` - HTML reports
   - `test-screenshots-*` - Failure screenshots
   - `test-logs-*` - Execution logs

**Direct Links:**
```
https://github.com/your-org/repo/actions/runs/<RUN_ID>
```

### Customization

Edit `.github/workflows/test.yml`:

**Change Python Versions:**
```yaml
python-version: ['3.10', '3.11', '3.12']  # Add/remove as needed
```

**Change Trigger Schedule:**
```yaml
schedule:
  - cron: '0 2 * * *'  # Change time (UTC)
```

**Add Different OS:**
```yaml
strategy:
  matrix:
    os: [macos-latest, macos-12]
```

---

## Jenkins

### Overview

The framework includes a Jenkinsfile for enterprise CI/CD at the root and detailed setup guide at `ci/JENKINS_SETUP.md`.

### Key Features

- **Parameterized Builds** - Choose test suite, workers, options
- **Pipeline Stages** - Clear execution steps with logging
- **Artifact Management** - Archive reports and screenshots
- **HTML Report Plugin** - Publish reports in Jenkins UI
- **Email Notifications** - Optional failure alerts
- **Environment Management** - Secure credential handling

### Setup Instructions

See `ci/JENKINS_SETUP.md` for complete instructions. Quick summary:

1. **Create Pipeline Job**
   - Jenkins Dashboard → New Item
   - Name: `santa-ios-automation`
   - Type: Pipeline

2. **Configure SCM**
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository: Your GitHub URL
   - Script Path: `Jenkinsfile`

3. **Add Parameters**
   - TEST_SUITE: all, smoke, regression, ntp, api
   - PARALLEL_EXECUTION: true/false
   - NUM_WORKERS: 1-4

4. **Configure Agent**
   - Label: `macos`
   - Ensure Node.js, Xcode, Python are installed

5. **Set Build Triggers**
   - GitHub Hook (recommended)
   - Poll SCM: `H H(0-5) * * *`
   - Build periodically: `H H(2) * * *`

### Build Parameters

```groovy
parameters {
    choice(name: 'TEST_SUITE', choices: ['all', 'smoke', 'regression', 'ntp', 'api'])
    booleanParam(name: 'PARALLEL_EXECUTION', defaultValue: true)
    string(name: 'NUM_WORKERS', defaultValue: '2')
}
```

### View Results

**In Jenkins UI:**
1. Dashboard → Job name
2. Click build number
3. View "Console Output"
4. Click "pytest HTML Report" for test details
5. Check "Artifacts" for reports/screenshots

**Build Status Indicators:**
- ✅ **Blue** - All tests passed
- 🟡 **Yellow** - Some tests failed
- ❌ **Red** - Build failed or error

---

## General Best Practices

### 1. Environment Management

**Use environment variables, not hardcoded values:**

```yaml
# GitHub Actions
env:
  APPIUM_HOST: '127.0.0.1'
  APPIUM_PORT: '4723'
```

```groovy
// Jenkins
environment {
    APPIUM_HOST = '127.0.0.1'
    APPIUM_PORT = '4723'
}
```

**Store secrets securely:**

```yaml
# GitHub Actions
env:
  DEVICE_UDID: ${{ secrets.DEVICE_UDID }}
```

```groovy
// Jenkins
environment {
    DEVICE_CREDENTIALS = credentials('device-udid')
}
```

### 2. Dependency Management

**Always pin versions:**

```
pytest==7.4.3
pytest-xdist==3.5.0
pytest-html==4.2.0
Appium-Python-Client==3.1.0
```

**Use requirements.txt for consistency:**

```bash
pip install -r requirements.txt --no-deps
```

### 3. Appium Server Lifecycle

**Always manage server lifecycle:**

```bash
# Start with logging
appium --port 4723 > appium.log 2>&1 &

# Wait for readiness
for i in {1..30}; do
  if curl -s http://127.0.0.1:4723/status > /dev/null; then
    echo "Appium ready"
    break
  fi
  sleep 2
done

# Tests run here...

# Always cleanup
pkill -f appium || true
```

### 4. Report Generation

**Always generate reports:**

```bash
pytest tests/ \
  --html=reports/report.html \
  --self-contained-html \
  --junit-xml=reports/junit.xml
```

**Archive artifacts:**

```yaml
# GitHub Actions
- uses: actions/upload-artifact@v4
  with:
    name: test-report
    path: reports/
    retention-days: 30
```

### 5. Test Isolation

**Each test should be independent:**

```python
@pytest.fixture(autouse=True)
def cleanup(driver):
    """Cleanup after each test."""
    yield
    # Teardown code here
    driver.reset()
```

### 6. Parallel Execution

**Use worker-safe locking for shared resources:**

```python
# conftest.py includes device locking
import fcntl

lock_file = open("/tmp/appium_device.lock", "w+")
fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
# Test runs with exclusive access
fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
```

**Run with optimal worker count:**

```bash
# 2-4 workers usually optimal
pytest -n 2 tests/

# Check system resources
grep -c ^processor /proc/cpuinfo
```

### 7. Logging and Monitoring

**Capture comprehensive logs:**

```python
from utils.logger import get_logger

logger = get_logger()

def test_example(driver):
    logger.info("Test started")
    logger.debug("Detailed info")
    logger.error("Error occurred")
```

**Store logs for analysis:**

```
reports/logs/test.log  # Test execution logs
reports/appium.log     # Appium server logs
```

### 8. Failure Handling

**Capture evidence on failure:**

```python
# Automatic in conftest.py
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Screenshots automatically captured
    # Logs automatically attached
```

### 9. Test Data Management

**Keep test data separate from test code:**

```
tests/
├── data/
│   ├── test_data.py
│   ├── fixtures.json
│   └── credentials.json
├── test_example.py
```

```python
from tests.data.test_data import TEST_URLS

def test_navigation(driver):
    driver.get(TEST_URLS['homepage'])
```

### 10. Notification Strategy

**Notify on failures:**

```yaml
# GitHub Actions - Slack
- name: Notify on Failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

```groovy
// Jenkins - Email
post {
    failure {
        emailext(subject: 'Tests Failed',
                 body: 'Check: $BUILD_URL')
    }
}
```

---

## Troubleshooting

### GitHub Actions

**Problem:** Tests timeout

```yaml
# Increase timeout in workflow
jobs:
  test:
    timeout-minutes: 45  # Increase from 30
```

**Problem:** Appium won't start

```yaml
# Check logs
- name: Check Appium
  run: appium --version
  
# Start with explicit config
- name: Start Appium
  run: |
    appium \
      --port 4723 \
      --log-level debug \
      --log-timestamp \
      > appium.log 2>&1 &
```

**Problem:** Artifacts not found

```yaml
# Use if-no-files-found
- uses: actions/upload-artifact@v4
  with:
    path: reports/
    if-no-files-found: ignore  # Don't fail if missing
```

### Jenkins

**Problem:** Pipeline fails to run

```groovy
// Check agent availability
options {
    timestamps()
    timeout(time: 1, unit: 'HOURS')
}

// Validate Groovy syntax
// Jenkins → Manage Jenkins → In-process Script Approval
```

**Problem:** Appium server issues

```bash
# Clear old processes
pkill -f appium || true
sleep 2

# Start fresh
appium --port 4723 --allow-insecure adb --allow-insecure chromedriver
```

**Problem:** Permission errors

```bash
# Fix Xcode permissions
sudo xcode-select --reset
sudo xcode-select --install
sudo xcodebuild -license accept
```

---

## Performance Optimization

### Reduce CI Time

**Use parallel workers:**
```bash
pytest -n 4 tests/  # 4 parallel workers
```

**Run only affected tests:**
```bash
# Only run smoke tests
pytest -m smoke tests/
```

**Cache dependencies:**
```yaml
# GitHub Actions
- uses: actions/setup-python@v4
  with:
    cache: 'pip'  # Auto-cache requirements
```

```groovy
// Jenkins - use Docker or persistent agent
```

### Optimize Resource Usage

**Memory:**
```bash
# Monitor during execution
watch -n 1 'ps aux | grep appium'
```

**Disk Space:**
```bash
# Clean old artifacts
artifactRetentionDays: 30  # Auto-cleanup
```

---

## Security

### Protect Secrets

**GitHub Actions:**
```yaml
env:
  DEVICE_UDID: ${{ secrets.DEVICE_UDID }}  # Never in code
```

**Jenkins:**
```groovy
withCredentials([string(credentialsId: 'device-udid', variable: 'UDID')]) {
    // Use $UDID variable
}
```

### Limit Access

**GitHub Actions:**
- Protect main/develop branches
- Require PR reviews
- Limit action permissions

**Jenkins:**
- Configure security realm
- Set job permissions
- Audit build logs

---

## Monitoring and Alerts

### Success Metrics

- Test pass rate
- Average execution time
- Failure screenshots captured
- Report generation time

### Alert Conditions

- Build failure
- Test timeout
- Low pass rate (< 95%)
- Slow tests (> 30s)
- Server errors

### Dashboard Setup

**GitHub:**
- Use "Status Checks" in branch protection
- Create custom dashboards with GitHub Insights

**Jenkins:**
- Install Dashboard plugin
- Create trending graphs
- Set up email/Slack integration

---

## References

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Jenkins Pipeline Guide](https://www.jenkins.io/doc/book/pipeline/)
- [Appium Server Documentation](https://appium.io/docs/en/latest/quickstart/install/)
- [pytest Documentation](https://docs.pytest.org/)
