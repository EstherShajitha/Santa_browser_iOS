import pytest
from pages.ntp_page import NTPPage

@pytest.mark.smoke
@pytest.mark.ntp
@pytest.mark.ui
def test_theme_changer(driver):
    ntp = NTPPage(driver)
    ntp.go_to_ntp()
    
    # Get initial theme state
    initial_theme = ntp.get_current_theme()
    
    # Click to change theme
    ntp.click_theme()
    
    # Verify theme changed
    after_theme = ntp.get_current_theme()
    assert initial_theme != after_theme, "Theme should have changed"
    
    # Revert to original theme
    ntp.click_theme()
    final_theme = ntp.get_current_theme()
    assert final_theme == initial_theme, "Theme should be reverted to initial state"
    
   