"""
Settings locators for preferences, toggles, and configuration screens
"""
from appium.webdriver.common.appiumby import AppiumBy


class SettingsLocators:
    """Locators for Settings screen and all preference toggles"""

    # Settings Navigation
    SETTINGS_MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "SettingsButton")
    SETTINGS_SCREEN_TITLE = (AppiumBy.IOS_PREDICATE, "name == 'Settings'")

    # General Settings
    LANGUAGE_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "LanguageToggle")
    THEME_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "ThemeToggle")

    # Privacy & Security
    PRIVACY_SETTINGS_ROW = (AppiumBy.ACCESSIBILITY_ID, "PrivacySettings")
    CLEAR_BROWSING_DATA_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "ClearBrowsingDataButton")

    # Sync & Account
    SYNC_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "SyncToggle")
    SIGN_IN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "SignInButton")

    # About
    ABOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "AboutButton")
    VERSION_TEXT = (AppiumBy.IOS_PREDICATE, "label CONTAINS 'Version'")
