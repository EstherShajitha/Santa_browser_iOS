import pytest
from pages.ntp_page import NTPPage

@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui
def test_rewards_navigation(driver):

    ntp = NTPPage(driver)

    ntp.go_to_ntp()
    ntp.click_rewards()
    ntp.click_back()
    ntp.verify_ntp_loaded()


@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui
def test_cashback_navigation(driver):

    ntp = NTPPage(driver)

    ntp.go_to_ntp()
    ntp.click_cashback()
    ntp.click_back()
    ntp.verify_ntp_loaded()