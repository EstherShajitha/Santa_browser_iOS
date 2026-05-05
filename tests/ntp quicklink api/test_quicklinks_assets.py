import requests
from utils.api_client import get_quicklinks


def test_quicklinks_icons():

    data = get_quicklinks()

    broken_icons = []

    for app in data["apps"]:

        name = app.get("name")
        icon = app.get("icon")

        try:
            r = requests.get(icon, timeout=10)

            if r.status_code != 200:
                broken_icons.append(f"{name} → {r.status_code}")

        except Exception as e:
            broken_icons.append(f"{name} → {str(e)}")

    if broken_icons:
        print("\nBROKEN ICONS:")
        for icon in broken_icons:
            print(icon)

    assert len(broken_icons) == 0