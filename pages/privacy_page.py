"""
Privacy page class for ad blocker, private mode, VPN, and tracking protection interactions
"""
from pages.base_page import BasePage
from locators.privacy_locators import PrivacyLocators
from selenium.webdriver.support import expected_conditions as EC


class PrivacyPage(BasePage):
    """Page object for privacy and security features"""

    def __init__(self, driver):
        super().__init__(driver)

    # Ad Blocker
    def toggle_ad_blocker(self):
        """Toggle ad blocker on/off"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.AD_BLOCKER_TOGGLE)
        ).click()

    def open_ad_blocker_settings(self):
        """Open ad blocker settings"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.AD_BLOCKER_SETTINGS)
        ).click()

    def get_blocked_ads_count(self) -> str:
        """Get number of ads blocked"""
        status = self.wait.until(
            EC.presence_of_element_located(PrivacyLocators.AD_BLOCKER_STATUS)
        )
        return status.text

    # Private Mode
    def toggle_private_mode(self):
        """Toggle private/incognito mode"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.PRIVATE_MODE_TOGGLE)
        ).click()

    def is_private_mode_active(self) -> bool:
        """Check if private mode is currently active"""
        try:
            self.wait.until(
                EC.visibility_of_element_located(PrivacyLocators.PRIVATE_MODE_INDICATOR)
            )
            return True
        except Exception:
            return False

    def exit_private_mode(self):
        """Exit private mode"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.EXIT_PRIVATE_MODE)
        ).click()

    # VPN
    def toggle_vpn(self):
        """Toggle VPN on/off"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.VPN_TOGGLE)
        ).click()

    def is_vpn_connected(self) -> bool:
        """Check if VPN is connected"""
        try:
            self.wait.until(
                EC.visibility_of_element_located(PrivacyLocators.VPN_STATUS)
            )
            return True
        except Exception:
            return False

    def get_vpn_location(self) -> str:
        """Get current VPN location"""
        location = self.wait.until(
            EC.presence_of_element_located(PrivacyLocators.VPN_LOCATION)
        )
        return location.text

    # Tracking Protection
    def toggle_tracking_protection(self):
        """Toggle tracking protection"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.TRACKING_PROTECTION_TOGGLE)
        ).click()

    def get_trackers_blocked_count(self) -> str:
        """Get number of trackers blocked"""
        tracker_count = self.wait.until(
            EC.presence_of_element_located(PrivacyLocators.TRACKER_COUNT)
        )
        return tracker_count.text

    # Cookies & Site Data
    def toggle_cookies(self):
        """Toggle cookie handling"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.COOKIES_TOGGLE)
        ).click()

    def clear_site_data(self):
        """Clear site data"""
        self.wait.until(
            EC.element_to_be_clickable(PrivacyLocators.SITE_DATA_BUTTON)
        ).click()
