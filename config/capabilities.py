from appium import webdriver
from appium.options.ios import XCUITestOptions
import pytest

APPIUM_SERVER = "http://127.0.0.1:4723"




def get_ios_options(worker_index=0):
    options = XCUITestOptions()

    options.platform_name = "iOS"
    options.device_name = "iPhone"
    options.platform_version = "17.5"
    options.udid = "00008101-001C656A0211A01E"
    options.bundle_id = "org.santa.ios.browser"
    options.automation_name = "XCUITest"
    options.no_reset = True

    # Optional unique ports for parallel execution
    options.set_capability("wdaLocalPort", 8100 + worker_index)
    options.set_capability("mjpegServerPort", 9100 + worker_index)

    return options