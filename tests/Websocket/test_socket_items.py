import pytest
import requests
import uuid
import time

from selenium.webdriver.support.ui import WebDriverWait

from config.environment import PUSH_API_URL
from pages.websocket_page import Websocketspage


@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui
def test_socket_items(driver):

    websockets = Websocketspage(driver)

    clid = "f33fb36d5a592c0"
    msg_id = str(uuid.uuid4())

    payload = {
        "audience": {
            "clids": [clid]
        },
        "envelope": {
            "v": 1,
            "msg_id": msg_id,
            "type": "in_app_nudge",
            "category": "promotions",
            "payload": {
                "display": {
                    "style": "bottomsheet",
                    "title": "Recommended for you",
                    "items": [
                        {
                            "kind": "product",
                            "title": "Nike Air Max",
                            "image": "https://notify-dev.santabrowser.com/banner.png",
                            "price": "₹7,999",
                            "payout_label": "Earn ₹120",
                            "deeplink": "https://shopping.santabrowser.com"
                        },
                        {
                            "kind": "product",
                            "title": "Nike Air Max",
                            "image": "https://notify-dev.santabrowser.com/banner.png",
                            "price": "₹7,999",
                            "payout_label": "Earn ₹120",
                            "deeplink": "https://shopping.santabrowser.com"
                        },
                        {
                            "kind": "product",
                            "title": "Nike Air Max",
                            "image": "https://notify-dev.santabrowser.com/banner.png",
                            "price": "₹7,999",
                            "payout_label": "Earn ₹120",
                            "deeplink": "https://shopping.santabrowser.com"
                        },
                        {
                            "kind": "product",
                            "title": "Nike Air Max",
                            "image": "https://notify-dev.santabrowser.com/banner.png",
                            "price": "₹7,999",
                            "payout_label": "Earn ₹120",
                            "deeplink": "https://shopping.santabrowser.com"
                        }
                    ]
                }
            }
        },
        "delivery": "ws"
    }

    headers = {
        "x-admin-key": "44af092bd0024d2d9f3ce7cc911c69d1",
        "Content-Type": "application/json"
    }

    try:

        response = requests.post(
            PUSH_API_URL,
            json=payload,
            headers=headers
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        assert response.status_code == 200

        time.sleep(5)

        # Bottomsheet title
        actual_title = websockets.get_bottomsheet_title()
        print("Bottomsheet Title:", actual_title)

        # First Item
        first_title = websockets.get_first_item_title()
        first_price = websockets.get_first_item_price()
        first_payout = websockets.get_first_item_payout()

        print("First Item Title:", first_title)
        print("First Item Price:", first_price)
        print("First Item Payout:", first_payout)

        # Second Item
        second_title = websockets.get_second_item_title()
        second_price = websockets.get_second_item_price()
        second_payout = websockets.get_second_item_payout()

        print("Second Item Title:", second_title)
        print("Second Item Price:", second_price)
        print("Second Item Payout:", second_payout)

        # Third Item
        third_title = websockets.get_third_item_title()
        third_price = websockets.get_third_item_price()
        third_payout = websockets.get_third_item_payout()

        print("Third Item Title:", third_title)
        print("Third Item Price:", third_price)
        print("Third Item Payout:", third_payout)

        # Fourth Item
        fourth_title = websockets.get_fourth_item_title()
        fourth_price = websockets.get_fourth_item_price()
        fourth_payout = websockets.get_fourth_item_payout()

        print("Fourth Item Title:", fourth_title)
        print("Fourth Item Price:", fourth_price)
        print("Fourth Item Payout:", fourth_payout)

        # Click only first item CTA
        websockets.click_first_item()

        print("First item clicked successfully")

        # Validate deeplink redirection
        WebDriverWait(driver, 10).until(
            lambda d: "shopping" in d.page_source.lower()
        )

        page_source = driver.page_source

        assert "shopping" in page_source.lower()

        print("CTA deeplink validated successfully")

    finally:

        websockets.cleanup_websocket_popup()