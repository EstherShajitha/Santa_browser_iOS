import pytest
import requests
import uuid
import time

from config.environment import PUSH_API_URL
from pages.websocket_page import Websocketspage


@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui
def test_websocket_CTA(driver):

    Websockets = Websocketspage(driver)

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
            "category": "rewards",
            "payload": {
                "display": {
                    "style": "bottomsheet",
                    "title": "Daily Check-in",
                    "body": "Don't lose your streak!",
                    "cta": {
                        "label": "Check-in Now",
                        "deeplink": "https://rewards.santabrowser.com"
                    }
                }
            }
        },
        "delivery": "ws"
    }

    # Expected values
    expected_title = payload["envelope"]["payload"]["display"]["title"]
    expected_body = payload["envelope"]["payload"]["display"]["body"]
    expected_deeplink = payload["envelope"]["payload"]["display"]["cta"]["deeplink"]

    headers = {
        "x-admin-key": "44af092bd0024d2d9f3ce7cc911c69d1",
        "Content-Type": "application/json"
    }

    # Send push notification
    response = requests.post(
        PUSH_API_URL,
        json=payload,
        headers=headers
    )

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    # Validate API response
    assert response.status_code == 200

    # Wait for notification
    time.sleep(5)

    # Validate title and body
    actual_title = Websockets.socket_text_cta()
    actual_body = Websockets.socket_body_cta()

    print("Expected Title:", expected_title)
    print("Actual Title:", actual_title)

    print("Expected Body:", expected_body)
    print("Actual Body:", actual_body)

    assert actual_title == expected_title
    assert actual_body == expected_body

    # Click CTA
    Websockets.socket_cta()

# Wait briefly for redirection
    time.sleep(3)

# Validate redirected page loaded
    page_source = driver.page_source

    print("Page Loaded Successfully")

# Validate deeplink destination content
    assert "Rewards" in page_source or "rewards" in page_source.lower()

    print("CTA Deeplink validated successfully")