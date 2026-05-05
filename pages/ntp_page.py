
from pages.base_page import BasePage
from locators.ntp_locators import NTPLocators
from selenium.webdriver.support import expected_conditions as EC


class NTPPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    # -----------------------------------
    # STATE CONTROL
    # -----------------------------------

    def go_to_ntp(self):
        """
        Ensures we are on NTP before test starts.
        Press back if needed until search bar visible.
        """
        for _ in range(3):
            try:
                if self.driver.find_element(*NTPLocators.SEARCH_BAR).is_displayed():
                    return
            except Exception:
                pass

            try:
                self.driver.find_element(*NTPLocators.BACK_BUTTON).click()
            except Exception:
                break

        self.wait.until(
            EC.presence_of_element_located(NTPLocators.SEARCH_BAR)
        )

    def verify_ntp_loaded(self):
       
        return self.is_element_visible(NTPLocators.SEARCH_BAR)
    

    def is_search_bar_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(NTPLocators.SEARCH_BAR)
            )
            return True
        except Exception:
            return False

    # -----------------------------------
    # SEARCH FLOW
    # -----------------------------------

    def open_search(self):
        """Tap fake omnibox"""
        search_bar = self.wait.until(
            EC.presence_of_element_located(NTPLocators.SEARCH_BAR)
            )
        search_bar.click()

    def get_search_placeholder(self):
        element = self.wait.until(
            EC.presence_of_element_located(NTPLocators.SEARCH_BAR)
            )
        return element.text

    def is_keyboard_open(self) -> bool:
        try:
            self.wait.until(
                EC.presence_of_element_located(NTPLocators.KEYBOARD_BUTTON)
            )
            return True
        except Exception:
            return False

    def enter_search(self, text):
        field = self.wait.until(
            EC.presence_of_element_located(NTPLocators.SEARCH_FIELD)
        )
        field.clear()
        field.send_keys(text)
        field.send_keys("\n")

    def wait_for_url_contains(self, text):
        def check_url(driver):
            address_bar = driver.find_element(*NTPLocators.SEARCH_BAR)
            return text.lower() in address_bar.text.lower()

        self.wait.until(check_url)
    def get_address_bar_text(self):
        address_bar = self.driver.find_element(*NTPLocators.SEARCH_BAR)
        return address_bar.text
    # -----------------------------------
    # REWARDS FLOW
    # -----------------------------------

    def click_rewards(self):
        self.wait.until(
            EC.presence_of_element_located(NTPLocators.REWARDS_BUTTON)
        ).click()

    def is_rewards_page_loaded(self):
        return "rewards" in self.driver.current_url

    # -----------------------------------
    # CASHBACK FLOW
    # -----------------------------------

    def click_cashback(self):
        self.wait.until(
            EC.presence_of_element_located(NTPLocators.CASHBACK_BUTTON)
        ).click()

    # -----------------------------------
    # NAVIGATION
    # -----------------------------------

    def click_back(self):
        self.wait.until(
            EC.presence_of_element_located(NTPLocators.BACK_BUTTON)
        ).click()

    # -----------------------------------
    # TRACKER
    # -----------------------------------

    def get_tracker_count(self):
        try:
            tracker_elem = self.wait.until(
                EC.presence_of_element_located(NTPLocators.TRACKER_COUNT)
            )
            return tracker_elem.text
        except Exception:
            return None

    def is_tracker_count_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(NTPLocators.TRACKER_COUNT)
            )
            return True
        except Exception:
            return False

    # -----------------------------------
    # WEATHER
    # -----------------------------------

    def get_weather(self):
        try:
            weather_elem = self.wait.until(
                EC.presence_of_element_located(NTPLocators.WEATHER_INFO)
            )
            return weather_elem.text
        except Exception:
            return None

    def is_weather_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(NTPLocators.WEATHER_INFO)
            )
            return True
        except Exception:
            return False

    # -----------------------------------
    # TOOLBAR
    # -----------------------------------

    def open_toolbar(self):
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.TOOLBAR_BUTTON)
        ).click()

    def is_toolbar_open(self):
        try:
            self.wait.until(
                EC.visibility_of_element_located(NTPLocators.TOOLBAR_BUTTON)
            )
            return True
        except Exception:
            return False

    def close_bottom_sheet(self):
        self.driver.execute_script(
            "mobile: swipe",
            {
                "direction": "down",
                "velocity": 1000
            }
        )

    def is_bottom_sheet_visible(self) -> bool:
        try:
            self.wait.until(
                EC.visibility_of_element_located(NTPLocators.SHEET_GRABBER)
            )
            return True
        except Exception:
            return False
    #theme changer
    def click_theme(self):
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.THEME_BUTTON)
            ).click()
    
    def get_current_theme(self):
        """Get current theme state from theme button attribute"""
        theme_btn = self.wait.until(
            EC.presence_of_element_located(NTPLocators.THEME_BUTTON)
        )
        return theme_btn.get_attribute("name")
    
    def toggle_theme(self):
        """Toggle theme (Light <-> Dark)"""
        theme_btn = self.wait.until(
            EC.element_to_be_clickable(NTPLocators.THEME_BUTTON)
            )

        current_theme = theme_btn.get_attribute("name")

    # First click
        theme_btn.click()

    # Wait until theme icon changes
        self.wait.until(
            lambda d: d.find_element(*NTPLocators.THEME_BUTTON).get_attribute("name") != current_theme
       )

    # Click again to revert theme
        self.driver.find_element(*NTPLocators.THEME_BUTTON).click()

    def coinwatchlist_menu(self):
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.COIN_WATCHLIST)
            ).click()
    def ntp_scroll(self):
        """Scroll NTP page to view news feed"""
        scrollable = self.wait.until(
            EC.presence_of_element_located(NTPLocators.NTP_SCROLL)
            )
        self.driver.execute_script(
            "mobile: swipe",
            {
                "direction": "up",
                "velocity": 2000
          }
          )
    def scroll_to_top(self):
        """Scroll to top of NTP by tapping the top toolbar button"""
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.scroll_top)
            ).click()    
    def open_cashrewards_widget(self): 
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.CASHREWARDS_WIDGET)
            ).click()
    def click_add_tab(self):
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.ADD_TAB_BUTTON)
            ).click()

    def create_new_tab(self):
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.CREATE_NEWTAB)
            ).click()
    def is_rewards_page_opened(self):
         return self.is_element_visible(NTPLocators.rewards_address_bar)
    def click_rewards_icon(self):
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.rewards_icon)
            ).click()
    def add_quicklinks(self):
        self.wait.until(
            EC.element_to_be_clickable(NTPLocators.Add_Quicklink)
            ).click()    