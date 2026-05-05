import pytest
from pages.ntp_page import NTPPage

@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui
def test_coinwatchlist_menu(driver):
    ntp= NTPPage(driver)
    ntp.go_to_ntp()
    ntp.coinwatchlist_menu()
    ntp.click_back()
    ntp.verify_ntp_loaded()