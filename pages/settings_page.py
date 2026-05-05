"""
Settings page class for preferences, toggles, and configuration screen interactions
"""
from pages.base_page import BasePage
from locators.settings_locators import SettingsLocators
from selenium.webdriver.support import expected_conditions as EC


class SettingsPage(BasePage):
    """Page object for Settings screen and preference toggles"""

    def __init__(self, driver):
        super().__init__(driver)

    # Navigation
    def open_settings(self):
        """Open the Settings screen"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.SETTINGS_MENU_BUTTON)
        ).click()

    def wait_for_settings_screen(self):
        """Wait for Settings screen to appear"""
        self.wait.until(
            EC.presence_of_element_located(SettingsLocators.SETTINGS_SCREEN_TITLE)
        )

    # General Settings
    def toggle_language(self):
        """Toggle language setting"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.LANGUAGE_TOGGLE)
        ).click()

    def toggle_theme(self):
        """Toggle theme setting (light/dark)"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.THEME_TOGGLE)
        ).click()

    # Privacy Settings
    def open_privacy_settings(self):
        """Navigate to privacy settings"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.PRIVACY_SETTINGS_ROW)
        ).click()

    def clear_browsing_data(self):
        """Clear browsing data"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.CLEAR_BROWSING_DATA_BUTTON)
        ).click()

    # Sync & Account
    def toggle_sync(self):
        """Toggle sync setting"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.SYNC_TOGGLE)
        ).click()

    def click_sign_in(self):
        """Click sign in button"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.SIGN_IN_BUTTON)
        ).click()

    # About
    def open_about(self):
        """Open About screen"""
        self.wait.until(
            EC.element_to_be_clickable(SettingsLocators.ABOUT_BUTTON)
        ).click()

    def get_version(self) -> str:
        """Get app version"""
        version = self.wait.until(
            EC.presence_of_element_located(SettingsLocators.VERSION_TEXT)
        )
        return version.text
