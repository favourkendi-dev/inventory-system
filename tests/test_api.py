import json
from unittest.mock import patch, Mock
from app.external_api import ExternalAPIError


def test_get_inventory_empty(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_item_success(client):
    payload = {"name": "Notebook", "price": 3.50, "stock": 20}
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201

    data = response.get_json()
    assert data["name"] == "Notebook"
    assert data["price"] == 3.50
    assert data["stock"] == 20
    assert "id" in data  # server-assigned


def test_create_item_missing_required_field(client):
    payload = {"name": "Broken Item", "stock": 5}
    response = client.post("/inventory", json=payload)
    assert response.status_code == 400
    assert "price" in response.get_json()["errors"]


def test_create_item_ignores_client_sent_id(client):
    payload = {"name": "Notebook", "price": 3.50, "stock": 20, "id": 999}
    response = client.post("/inventory", json=payload)
    data = response.get_json()
    assert data["id"] != 999


def test_get_item_by_id(client):
    create_response = client.post("/inventory", json={"name": "Pen", "price": 1.0, "stock": 100})
    item_id = create_response.get_json()["id"]

    response = client.get(f"/inventory/{item_id}")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Pen"


def test_get_item_not_found(client):
    response = client.get("/inventory/9999")
    assert response.status_code == 404


def test_update_item_stock(client):
    create_response = client.post("/inventory", json={"name": "Pen", "price": 1.0, "stock": 100})
    item_id = create_response.get_json()["id"]

    response = client.patch(f"/inventory/{item_id}", json={"stock": 50})
    assert response.status_code == 200
    assert response.get_json()["stock"] == 50
    assert response.get_json()["price"] == 1.0  # unchanged


def test_update_item_not_found(client):
    response = client.patch("/inventory/9999", json={"stock": 50})
    assert response.status_code == 404


def test_delete_item(client):
    create_response = client.post("/inventory", json={"name": "Pen", "price": 1.0, "stock": 100})
    item_id = create_response.get_json()["id"]

    response = client.delete(f"/inventory/{item_id}")
    assert response.status_code == 204
    
    get_response = client.get(f"/inventory/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/9999")
    assert response.status_code == 404

def test_lookup_no_params(client):
    response = client.get("/lookup")
    assert response.status_code == 400


def test_lookup_by_barcode_success(client):
    fake_product = {
        "name": "Nutella",
        "barcode": "3017620422003",
        "brands": "Ferrero",
        "categories": "Spreads",
        "image_url": "http://example.com/nutella.jpg",
    }

    with patch("app.routes.find_by_barcode", return_value=fake_product):
        response = client.get("/lookup?barcode=3017620422003")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Nutella"


def test_lookup_by_barcode_not_found(client):
    with patch("app.routes.find_by_barcode", return_value=None):
        response = client.get("/lookup?barcode=00000000000")

    assert response.status_code == 404


def test_lookup_by_name_success(client):
    fake_results = [{"name": "Nutella", "barcode": "111", "brands": "Ferrero",
                      "categories": "Spreads", "image_url": None}]

    with patch("app.routes.search_by_name", return_value=fake_results):
        response = client.get("/lookup?name=nutella")

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_lookup_external_api_failure(client):
    with patch("app.routes.find_by_barcode", side_effect=ExternalAPIError("API is down")):
        response = client.get("/lookup?barcode=3017620422003")

    assert response.status_code == 502
    assert "error" in response.get_json()