"""
Browser page class for URL navigation, tabs, and browser chrome interactions
"""
from pages.base_page import BasePage
from locators.browser_locators import BrowserLocators
from selenium.webdriver.support import expected_conditions as EC


class BrowserPage(BasePage):
    """Page object for browser navigation controls and URL bar"""

    def __init__(self, driver):
        super().__init__(driver)

    # Address Bar / URL Navigation
    def navigate_to_url(self, url: str):
        """Navigate to a URL by entering it in the address bar"""
        address_bar = self.wait.until(
            EC.element_to_be_clickable(BrowserLocators.ADDRESS_BAR)
        )
        address_bar.click()
        url_input = self.wait.until(
            EC.presence_of_element_located(BrowserLocators.URL_INPUT_FIELD)
        )
        url_input.clear()
        url_input.send_keys(url)
        url_input.send_keys("\n")

    def get_current_url(self) -> str:
        """Get the current URL from the address bar"""
        address_bar = self.wait.until(
            EC.presence_of_element_located(BrowserLocators.ADDRESS_BAR)
        )
        return address_bar.text

    # Navigation Controls
    def click_back(self):
        """Click the back button"""
        self.wait.until(
            EC.element_to_be_clickable(BrowserLocators.BACK_BUTTON)
        ).click()

    def click_forward(self):
        """Click the forward button"""
        self.wait.until(
            EC.element_to_be_clickable(BrowserLocators.FORWARD_BUTTON)
        ).click()

    def click_refresh(self):
        """Click the refresh button"""
        self.wait.until(
            EC.element_to_be_clickable(BrowserLocators.REFRESH_BUTTON)
        ).click()

    # Tab Management
    def open_new_tab(self):
        """Open a new tab"""
        self.wait.until(
            EC.element_to_be_clickable(BrowserLocators.NEW_TAB_BUTTON)
        ).click()

    def open_tab_switcher(self):
        """Open the tab switcher"""
        self.wait.until(
            EC.element_to_be_clickable(BrowserLocators.TAB_SWITCHER)
        ).click()

    # Loading States
    def wait_for_page_load(self):
        """Wait for page to finish loading"""
        self.wait.until_not(
            EC.presence_of_element_located(BrowserLocators.LOADING_INDICATOR)
        )
