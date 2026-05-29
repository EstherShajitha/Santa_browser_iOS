from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.websocket_locators import Websocketlocators
from appium.webdriver.common.appiumby import AppiumBy
import time


class Websocketspage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def socket_text_cta(self):
        try:
            element = self.wait.until(
                EC.presence_of_element_located(
                    Websocketlocators.Text_CTA_TITLE
                )
            )
            return element.text

        except Exception as e:
            print(f"Title not found: {e}")
            return None

    def socket_body_cta(self):
        try:
            element = self.wait.until(
                EC.presence_of_element_located(
                    Websocketlocators.Text_CTA_BODY
                )
            )
            return element.text

        except Exception as e:
            print(f"Body not found: {e}")
            return None

    def socket_cta(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(
                    Websocketlocators.Text_CTA_CTA
                )
            ).click()

            return True

        except Exception as e:
            print(f"CTA button not clickable: {e}")
            return False
    def image_title_cta(self):
        try:
            element = self.wait.until(
                EC.presence_of_element_located(
                    Websocketlocators.Image_CTA_TITLE
                )
            )
            return element.text

        except Exception as e:
            print(f"Title not found: {e}")
            return None
    def image_body_cta(self):
        try:
            element = self.wait.until(
                EC.presence_of_element_located(Websocketlocators.Image_CTA_BODY
                )
            )
            return element.text
        except Exception as e:
            print(f"Body not found: {e}")
            return None
    def image_cta_button(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(Websocketlocators.Image_CTA_CTA)
            ).click()
            return True
        except Exception as e:
            print(f"CTA button not clickable: {e}")
            return False
    
    def image_cta_image(self):
        try:
            element = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(Websocketlocators.Image_CTA
                )
            ).click()

            print("Image CTA is present and clickable")
            return element

        except Exception as e:
            print(f"Image CTA not clickable: {e}")
            return None
    def cleanup_websocket_popup(self):
        try:
            self.wait.until(
                EC.element_to_be_clickable(Websocketlocators.xmark)
            ).click()
            return True
        except TimeoutException:

            print("No websocket popup present")

            return False
        except Exception as e:
            print(f"Close button not clickable: {e}")
            return False
        
     # ITEMS
    def get_bottomsheet_title(self):
        try:
            element= self.wait.until(
                EC.presence_of_element_located(Websocketlocators.BOTTOM_SHEET_TITLE)
                )
            return element.text

        except Exception as e:
            print(f"Title not found: {e}")
            return None
    def get_first_item_title(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.FIRST_ITEMS_NAME)
            )
            return element.text
        except Exception as e:
            print(f"Title not found: {e}")
            return None 
    def get_first_item_price(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.FIRST_ITEMS_PRICE)
            )
            return element.text
        except Exception as e:
            print(f"Price not found: {e}")
            return None
    def get_first_item_payout(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.FIRST_ITEMS_PAYOUT)
            )
            return element.text
        except Exception as e:
            print(f"Payout not found: {e}")
            return None
    def click_first_item(self):
        try:
            element=self.wait.until(
                EC.element_to_be_clickable(Websocketlocators.FIRST_ITEMS_NAME)
            )
            element.click()
            return element
        except Exception as e:
            print(f"First item not clickable: {e}")
            return None        
    def get_second_item_title(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.SECOND_ITEMS_NAME)
            )
            return element.text
        except Exception as e:
            print(f"Title not found: {e}")
            return None 
    def get_second_item_price(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.SECOND_ITEMS_PRICE)
            )
            return element.text
        except Exception as e:
            print(f"Price not found: {e}")
            return None
    def get_second_item_payout(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.SECOND_ITEMS_PAYOUT)
            )
            return element.text
        except Exception as e:
            print(f"Payout not found: {e}")
            return None
    def get_third_item_title(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.THIRD_ITEMS_NAME)
            )
            return element.text
        except Exception as e:
            print(f"Title not found: {e}")
            return None 
    def get_third_item_price(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.THIRD_ITEMS_PRICE)
            )
            return element.text
        except Exception as e:
            print(f"Price not found: {e}")
            return None
    def get_third_item_payout(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.THIRD_ITEMS_PAYOUT)
            )
            return element.text
        except Exception as e:
            print(f"Payout not found: {e}")
            return None  
    def get_fourth_item_title(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.FOURTH_ITEMS_NAME)
            )
            return element.text
        except Exception as e:
            print(f"Title not found: {e}")
            return None 
    def get_fourth_item_price(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.FOURTH_ITEMS_PRICE)
            )
            return element.text
        except Exception as e:
            print(f"Price not found: {e}")
            return None
    def get_fourth_item_payout(self):
        try:
            element=self.wait.until(
                EC.presence_of_element_located(Websocketlocators.FOURTH_ITEMS_PAYOUT)
            )
            return element.text
        except Exception as e:
            print(f"Payout not found: {e}")
            return None 
    def validate_offer_list_title(self):

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    Websocketlocators.OFFER_LIST_TITLE
                )
            )

            print("Offer list title visible")

            return element

        except Exception as e:

            print(f"Offer list title not visible: {e}")

            return None

    # -----------------------------------
    # Validate Offer List Body
    # -----------------------------------
    def validate_offer_list_body(self):

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    Websocketlocators.OFFER_LIST_BODY
                )
            )

            print("Offer list body visible")

            return element

        except Exception as e:

            print(f"Offer list body not visible: {e}")

            return None

    # -----------------------------------
    # Validate Offer 1 Title
    # -----------------------------------
    def validate_offer_1_title(self):

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    Websocketlocators.OFFER_1_TITLE
                )
            )

            print("Offer 1 title visible")

            return element

        except Exception as e:

            print(f"Offer 1 title not visible: {e}")

            return None

    # -----------------------------------
    # Validate Offer 1 Payout
    # -----------------------------------
    def validate_offer_1_payout(self):

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(
                    Websocketlocators.OFFER_1_PAYOUT
                )
            )

            print("Offer 1 payout visible")

            return element

        except Exception as e:

            print(f"Offer 1 payout not visible: {e}")

            return None

    # -----------------------------------
    # Click Offer 1
    # -----------------------------------
    def click_offer_1(self):

        try:
            element = self.wait.until(
                EC.element_to_be_clickable(
                    Websocketlocators.OFFER_1_TITLE
                )
            )

            element.click()

            print("Offer 1 clicked successfully")

            return True

        except Exception as e:

            print(f"Offer 1 click failed: {e}")

            return False


    

        
      

        



         


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def open_notification_center(self):
    #     print("Opening notification center...")

    #     size = self.driver.get_window_size()
    #     width = size["width"]
    #     height = size["height"]

    #     start_x = width // 2

    # # Start slightly below notch/status area
    #     start_y = int(height * 0.03)

    # # Drag halfway down
    #     end_y = int(height * 0.55)

    #     print(f"Screen: {width}x{height}")
    #     print(f"Swipe from ({start_x},{start_y}) to ({start_x},{end_y})")

    #     self.driver.execute_script(
    #          "mobile: dragFromToForDuration",
    #         {
    #         "duration": 1.5,
    #         "fromX": start_x,
    #         "fromY": start_y,
    #         "toX": start_x,
    #         "toY": end_y
    #         }
    #     )

    #     time.sleep(5)

    #     print("Current active app:")
    #     print(self.driver.execute_script("mobile: activeAppInfo"))
    # def wait_for_notification(self):
    #     return WebDriverWait(self.driver, 15).until(
    #         EC.presence_of_element_located(
    #             NotificationLocators.NOTIFICATION_POPUP
    #         )
    #     )

    # def get_notification_title(self):
    #     title = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             NotificationLocators.NOTIFICATION_TITLE
    #         )
    #     )
    #     return title.text

    # def get_notification_body(self):
    #     body = WebDriverWait(self.driver, 10).until(
    #         EC.presence_of_element_located(
    #             NotificationLocators.NOTIFICATION_BODY
    #         )
    #     )
    #     return body.text

    # def tap_notification(self):
    #     banner = WebDriverWait(self.driver, 10).until(
    #         EC.element_to_be_clickable(
    #             AppiumBy.IOS_PREDICATE,
    #             "name == 'ShortLook.Platter.Content.Seamless'"
    #         ) 
    #     )
    #     banner.click()