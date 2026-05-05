"""
Privacy locators for ad blocker, private mode, VPN, and tracking protection
"""
from appium.webdriver.common.appiumby import AppiumBy


class PrivacyLocators:
    """Locators for privacy and security features"""

    # Ad Blocker
    AD_BLOCKER_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "AdBlockerToggle")
    AD_BLOCKER_SETTINGS = (AppiumBy.ACCESSIBILITY_ID, "AdBlockerSettings")
    AD_BLOCKER_STATUS = (AppiumBy.IOS_PREDICATE, "name CONTAINS 'ads blocked'")

    # Private Mode / Incognito
    PRIVATE_MODE_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "PrivateModeToggle")
    PRIVATE_MODE_INDICATOR = (AppiumBy.ACCESSIBILITY_ID, "PrivateModeIndicator")
    EXIT_PRIVATE_MODE = (AppiumBy.ACCESSIBILITY_ID, "ExitPrivateMode")

    # VPN
    VPN_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "VPNToggle")
    VPN_STATUS = (AppiumBy.IOS_PREDICATE, "name CONTAINS 'VPN'")
    VPN_LOCATION = (AppiumBy.ACCESSIBILITY_ID, "VPNLocation")

    # Tracking Protection
    TRACKING_PROTECTION_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "TrackingProtectionToggle")
    TRACKER_COUNT = (AppiumBy.IOS_PREDICATE, "label CONTAINS 'trackers blocked'")

    # Cookies & Site Data
    COOKIES_TOGGLE = (AppiumBy.ACCESSIBILITY_ID, "CookiesToggle")
    SITE_DATA_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "ClearSiteData")
