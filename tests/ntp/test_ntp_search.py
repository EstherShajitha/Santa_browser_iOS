import pytest
from pages.ntp_page import NTPPage

@pytest.mark.smoke
@pytest.mark.ntp
@pytest.mark.ui
def test_ntp_search(driver):

    ntp = NTPPage(driver)

    ntp.go_to_ntp()
    ntp.open_search()
    ntp.enter_search("https://rewards.santabrowser.com")

    ntp.click_back()
    ntp.verify_ntp_loaded()