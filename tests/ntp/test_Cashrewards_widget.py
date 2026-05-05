import pytest
from xlsxwriter import url
from pages.ntp_page import NTPPage

@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui

def test_cashrewards_widget_navigation(driver):

    ntp = NTPPage(driver)

    ntp.go_to_ntp()
    ntp.open_cashrewards_widget()

    assert ntp.is_rewards_page_opened(), \
        "Cashrewards widget did not navigate to the correct page"
    ntp.click_rewards_icon()

    # ntp.click_back()

    # assert ntp.verify_ntp_loaded(), \
    #     "NTP did not load after navigating back"
