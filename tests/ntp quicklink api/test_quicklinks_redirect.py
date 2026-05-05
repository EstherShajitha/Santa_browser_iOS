import pytest
import requests
import urllib3
import time
from utils.api_client import get_quicklinks

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
}

@pytest.mark.api
@pytest.mark.regression
def test_quicklinks_redirect_status():

    data = get_quicklinks()
    apps = data.get("apps", [])

    print(f"\nTotal Quicklinks: {len(apps)}\n")

    working_links = []
    failed_links = []

    for app in apps:

        name = app.get("name")
        url = app.get("url")

        try:
            response = requests.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=15,
                verify=True
            )

            status = response.status_code
            final_url = response.url

            print(f"{name} | {status} | {final_url}")

            if status in [200, 301, 302, 401, 403]:
                working_links.append((name, final_url, status))
            else:
                failed_links.append((name, final_url, status))

        except Exception as e:

            print(f"{name} | ERROR | {str(e)}")
            failed_links.append((name, url, str(e)))

        time.sleep(1)   # prevents 429 rate limit

    print("\n✅ WORKING QUICKLINKS")
    for name, url, status in working_links:
        print(f"{name} | {status} | {url}")

    print("\n❌ NON-200 QUICKLINKS")
    for name, url, status in failed_links:
        print(f"{name} | {status} | {url}")

    assert len(failed_links) == 0, f"Failed Quicklinks: {failed_links}"