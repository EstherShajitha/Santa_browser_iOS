import requests
import urllib3

# Disable SSL warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API = "https://ntp.santabrowser.com/api/v1.5/stats/quick-apps?device=ios&country=IN"


def get_quicklinks():
    response = requests.get(API, timeout=10, verify=True)

    if response.status_code != 200:
        raise Exception(f"Quicklinks API failed: {response.status_code}")

    return response.json()