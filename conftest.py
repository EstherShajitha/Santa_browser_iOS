import os
import pytest
from datetime import datetime
from appium import webdriver
from config.capabilities import get_ios_options
from config.environment import APPIUM_SERVER

try:
    from pytest_html import extras as pytest_html_extras
except ImportError:
    pytest_html_extras = None

try:
    from utils.logger import get_logger
    logger = get_logger()
except Exception:
    logger = None


# Ensure required directories exist
os.makedirs("reports/screenshots", exist_ok=True)
os.makedirs("reports/logs", exist_ok=True)


@pytest.fixture(scope="function")
def driver(request):
    worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")

    try:
        idx = int(worker.replace("gw", ""))
    except Exception:
        idx = 0

    if logger:
        logger.info(f"Initializing driver for worker {worker}")

    options = get_ios_options(worker_index=idx)

    # Lock for single device execution
    import fcntl
    lock_path = "/tmp/appium_device.lock"
    lock_file = open(lock_path, "w+")

    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)

        driver = webdriver.Remote(command_executor=APPIUM_SERVER,options=options)
        # Attach driver for hooks
        request.node.driver = driver

        yield driver

    finally:
        try:
            driver.quit()
        except Exception:
            pass

        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()
        except Exception:
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Add readable description
    report.description = get_readable_test_description(item)

    # Capture ONLY actual test failure
    if report.when == "call" and report.failed:

        driver = getattr(item, "driver", None) or item.funcargs.get("driver", None)

        if driver:
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"{item.name}_{timestamp}.png"
                file_path = os.path.join("reports/screenshots", file_name)

                driver.save_screenshot(file_path)

                if pytest_html_extras:
                    report.extras = getattr(report, "extras", [])
                    report.extras.append(pytest_html_extras.image(file_path))

                if logger:
                    logger.error(f"Screenshot captured: {file_path}")

            except Exception as e:
                if logger:
                    logger.error(f"Screenshot capture failed: {e}")
        else:
            if logger:
                logger.warning("Driver not available for screenshot")

        # Attach per-test log file
        log_file = f"reports/logs/{item.name}.log"

        if os.path.exists(log_file) and pytest_html_extras:
            try:
                with open(log_file, "r") as f:
                    content = f.read()

                if content.strip():
                    report.extras = getattr(report, "extras", [])
                    report.extras.append(
                        pytest_html_extras.text(content, name=f"{item.name}.log")
                    )

            except Exception as e:
                if logger:
                    logger.error(f"Log attach failed: {e}")


# HTML Report Customization
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Description</th>")


def pytest_html_results_table_row(report, cells):
    description = getattr(report, "description", "")
    cells.insert(2, f"<td>{description}</td>")


# Smart Description Generator
def get_readable_test_description(item):
    # 1. Docstring
    if hasattr(item, "obj") and getattr(item.obj, "__doc__", None):
        doc = item.obj.__doc__.strip()
        if doc:
            return doc

    # 2. Marker
    marker = item.get_closest_marker("description")
    if marker:
        return marker.args[0]

    # 3. Function name fallback
    name = item.name.replace("test_", "")
    return name.replace("_", " ").capitalize()


@pytest.fixture(autouse=True)
def setup_logging_and_cleanup(request):
    """Per-test logging setup"""

    log_file = f"reports/logs/{request.node.name}.log"

    try:
        with open(log_file, "w") as f:
            f.write("")
    except Exception:
        pass

    request.node.driver = None

    def set_driver(driver):
        request.node.driver = driver

    request.node.set_driver = set_driver

    yield