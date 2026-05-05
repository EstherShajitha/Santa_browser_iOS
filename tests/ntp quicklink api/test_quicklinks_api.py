from utils.api_client import get_quicklinks

def test_api_structure():

    data = get_quicklinks()

    assert "apps" in data
    assert "categories" in data