import pytest
import requests
from unittest.mock import patch, Mock

from app.external_api import find_by_barcode, search_by_name, ExternalAPIError


def test_find_by_barcode_success():
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "code": "3017620422003",
            "brands": "Ferrero",
            "categories": "Spreads",
            "image_url": "http://example.com/nutella.jpg",
        },
    }

    with patch("app.external_api.requests.get", return_value=fake_response):
        result = find_by_barcode("3017620422003")

    assert result == {
        "name": "Nutella",
        "barcode": "3017620422003",
        "brands": "Ferrero",
        "categories": "Spreads",
        "image_url": "http://example.com/nutella.jpg",
    }


def test_find_by_barcode_not_found():
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"status": 0}

    with patch("app.external_api.requests.get", return_value=fake_response):
        result = find_by_barcode("00000000000")

    assert result is None


def test_find_by_barcode_network_failure():
    with patch("app.external_api.requests.get", side_effect=requests.ConnectionError("no internet")):
        with pytest.raises(ExternalAPIError):
            find_by_barcode("3017620422003")


def test_find_by_barcode_http_error():
    fake_response = Mock()
    fake_response.raise_for_status.side_effect = requests.HTTPError("503 Server Error")

    with patch("app.external_api.requests.get", return_value=fake_response):
        with pytest.raises(ExternalAPIError):
            find_by_barcode("3017620422003")


def test_search_by_name_success():
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "products": [
            {"product_name": "Nutella", "code": "111", "brands": "Ferrero", "categories": "Spreads", "image_url": None},
            {"product_name": "Nutella Plant-Based", "code": "222", "brands": "Ferrero", "categories": "Spreads", "image_url": None},
        ]
    }

    with patch("app.external_api.requests.get", return_value=fake_response):
        results = search_by_name("nutella")

    assert len(results) == 2
    assert results[0]["name"] == "Nutella"
    assert results[1]["name"] == "Nutella Plant-Based"


def test_search_by_name_no_results():
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"products": []}

    with patch("app.external_api.requests.get", return_value=fake_response):
        results = search_by_name("xyznonexistentproduct")

    assert results == []