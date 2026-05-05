"""
Browser locators for URL navigation, tabs, address bar, back/forward buttons
"""
from appium.webdriver.common.appiumby import AppiumBy


class BrowserLocators:
    """Locators for browser chrome and navigation controls"""

    # Address Bar / URL Navigation
    ADDRESS_BAR = (AppiumBy.ACCESSIBILITY_ID, "AddressBarAccessibilityID")
    URL_INPUT_FIELD = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeTextField[`label == 'URL'`]")

    # Navigation Buttons
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "BackButton")
    FORWARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "ForwardButton")
    REFRESH_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "RefreshButton")
    STOP_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "StopButton")

    # Tabs
    TAB_BAR = (AppiumBy.ACCESSIBILITY_ID, "TabBar")
    NEW_TAB_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "NewTabButton")
    TAB_SWITCHER = (AppiumBy.ACCESSIBILITY_ID, "TabSwitcher")

    # Loading States
    LOADING_INDICATOR = (AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeActivityIndicator'")
    PROGRESS_BAR = (AppiumBy.IOS_PREDICATE, "name CONTAINS 'Progress'")
