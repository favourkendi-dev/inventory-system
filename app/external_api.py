import requests

BASE_URL = "https://world.openfoodfacts.org"
TIMEOUT_SECONDS = 5

HEADERS = {
    "User-Agent": "InventoryManagementApp/1.0 (contact: favourkendi0@gmail.com)"
}


class ExternalAPIError(Exception):
    pass


def _normalize_product(raw_product):
    return {
        "name": raw_product.get("product_name") or "Unknown",
        "barcode": raw_product.get("code"),
        "brands": raw_product.get("brands"),
        "categories": raw_product.get("categories"),
        "image_url": raw_product.get("image_url"),
    }


def find_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}.json"
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ExternalAPIError(f"Failed to reach OpenFoodFacts: {e}")

    data = response.json()
    if data.get("status") != 1:
        return None

    return _normalize_product(data["product"])


def search_by_name(name, limit=5):
    url = f"{BASE_URL}/cgi/search.pl"
    params = {"search_terms": name, "json": 1, "page_size": limit}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT_SECONDS)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ExternalAPIError(f"Failed to reach OpenFoodFacts: {e}")

    data = response.json()
    products = data.get("products", [])
    return [_normalize_product(p) for p in products[:limit]]