import pytest
import requests
import uuid

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from config.environment import PUSH_API_URL
from pages.websocket_page import Websocketspage


@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui
def test_websocket_CTA(driver):

    websockets = Websocketspage(driver)

    try:

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
                        "image": "https://notify-dev.santabrowser.com/banner.png",
                        "cta": {
                            "label": "",
                            "deeplink": "https://santabrowser.com"
                        }
                    }
                }
            },
            "delivery": "ws"
        }

        expected_deeplink = (
            payload["envelope"]["payload"]["display"]["cta"]["deeplink"]
        )

        headers = {
            "x-admin-key": "44af092bd0024d2d9f3ce7cc911c69d1",
            "Content-Type": "application/json"
        }

        # Send websocket notification
        response = requests.post(
            PUSH_API_URL,
            json=payload,
            headers=headers
        )

        print("Status Code:", response.status_code)
        print("Response:", response.text)

        # Validate API response
        assert response.status_code == 200

        # Wait for websocket image CTA
        image = websockets.image_cta_image()

        assert image is not None, "Image CTA not found"

        print("Image CTA displayed successfully")

        # Click image CTA
        image.click()

        print("Clicked image CTA")

        # Wait for deeplink redirection
        WebDriverWait(driver, 10).until(
            lambda d: "santa" in d.page_source.lower()
        )

        page_source = driver.page_source

        print("Page redirected successfully")

        # Validate deeplink destination
        assert "santa" in page_source.lower()

        print("CTA deeplink validated successfully")

    finally:

        # Cleanup websocket popup
        websockets.cleanup_websocket_popup()