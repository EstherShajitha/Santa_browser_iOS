import pytest
from pages.ntp_page import NTPPage

@pytest.mark.regression
@pytest.mark.ntp
@pytest.mark.ui
def test_ntp_toolbar(driver):
    ntp = NTPPage(driver)
    ntp.go_to_ntp()
    ntp.open_toolbar()
    assert ntp.is_toolbar_open(), "Toolbar should be open after clicking the toolbar button"
    ntp.close_bottom_sheet()
    assert not ntp.is_bottom_sheet_visible(), "Bottom sheet should be closed after swipe down"