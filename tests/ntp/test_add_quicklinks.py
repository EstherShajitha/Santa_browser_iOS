import pytest
from pages.ntp_page import NTPPage

@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui

def test_add_quicklinks(driver):
    ntp = NTPPage(driver)
    ntp.go_to_ntp()
    ntp.add_quicklinks()
    ntp.click_back()
    ntp.verify_ntp_loaded()
  