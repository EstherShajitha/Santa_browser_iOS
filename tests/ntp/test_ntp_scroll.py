import pytest
from pages.ntp_page import NTPPage

@pytest.mark.smoke
@pytest.mark.ntp
@pytest.mark.ui
def test_ntp_scroll(driver):
    ntp = NTPPage(driver)
    ntp.go_to_ntp()

    ntp.ntp_scroll()
    ntp.scroll_to_top()
    
    # Assert that news/content is visible after scroll (not just search bar)
    assert ntp.verify_ntp_loaded()
