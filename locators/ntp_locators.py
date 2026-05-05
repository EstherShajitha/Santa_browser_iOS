from appium.webdriver.common.appiumby import AppiumBy

class NTPLocators:

    # Search
    SEARCH_BAR = (AppiumBy.ACCESSIBILITY_ID, "NTPHomeFakeOmniboxAccessibilityID")
    SEARCH_FIELD = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeTextField")
    KEYBOARD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "UIKeyboardLayoutStar Preview")

    # Bottom Panel
    REWARDS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Rewards")
    CASHBACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Cashback")

    # Navigation
    BACK_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Back")

    # NTP Verification
    SEARCH_PLACEHOLDER = (AppiumBy.ACCESSIBILITY_ID, "Search or type URL")

    #Theme changer
    THEME_BUTTON = (AppiumBy.IOS_PREDICATE,'name == "ic_lightmode" OR name == "ic_darkmode"')

    # Tracker (Adblock counter)
    # This locator finds a static text that contains digits (the count)
    # If you need a more specific locator, inspect the app using Appium Inspector
    TRACKER_COUNT = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label CONTAINS \"ads blocked\"`]/preceding-sibling::XCUIElementTypeStaticText[1]")

    # Weather
    WEATHER_INFO = (AppiumBy.IOS_CLASS_CHAIN, "**/XCUIElementTypeStaticText[`label CONTAINS '°'`]")
    
    # Toolbar
    TOOLBAR_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "kToolbarToolsMenuButtonIdentifier")
    SHEET_GRABBER =(AppiumBy.ACCESSIBILITY_ID, "PopoverDismissRegion")

    #coinwatchlist menu
    COIN_WATCHLIST = (AppiumBy.ACCESSIBILITY_ID, "reveal more")

    #NTP scroll
    NTP_SCROLL = (AppiumBy.IOS_PREDICATE,'name CONTAINS "Vertical scroll bar"')

    #cashrewards widget 
    CASHREWARDS_WIDGET = (AppiumBy.ACCESSIBILITY_ID, "Open rewards")
    rewards_address_bar=(AppiumBy.IOS_PREDICATE,"name CONTAINS 'rewards.santabrowser.com'")
    rewards_icon = (AppiumBy.ACCESSIBILITY_ID, "Rewards")


    #add new tab
    ADD_TAB_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "kToolbarStackButtonIdentifier")

    #create_new_tab_button
    CREATE_NEWTAB = (AppiumBy.ACCESSIBILITY_ID, "Create new tab")

    scroll_top = (AppiumBy.ACCESSIBILITY_ID, "kToolbarNewTabButtonIdentifier")

    #quicklinks
    Add_Quicklink = (AppiumBy.ACCESSIBILITY_ID, "Add")

