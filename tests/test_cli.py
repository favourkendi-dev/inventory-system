from unittest.mock import patch, Mock
import cli


def test_view_all_items_empty(capsys):
    fake_response = Mock()
    fake_response.json.return_value = []

    with patch("cli.requests.get", return_value=fake_response):
        cli.view_all_items()

    captured = capsys.readouterr()
    assert "Inventory is empty." in captured.out


def test_view_all_items_with_data(capsys):
    fake_response = Mock()
    fake_response.json.return_value = [
        {"id": 1, "name": "Notebook", "price": 3.5, "stock": 20, "barcode": None}
    ]

    with patch("cli.requests.get", return_value=fake_response):
        cli.view_all_items()

    captured = capsys.readouterr()
    assert "Notebook" in captured.out


def test_add_new_item_success(capsys):
    fake_response = Mock()
    fake_response.status_code = 201
    fake_response.json.return_value = {"id": 1, "name": "Notebook", "price": 3.5, "stock": 20}

  
    fake_inputs = ["Notebook", "3.50", "20", ""]

    with patch("builtins.input", side_effect=fake_inputs), \
         patch("cli.requests.post", return_value=fake_response) as mock_post:
        cli.add_new_item()

    # confirm the CLI sent the right payload to the API
    mock_post.assert_called_once()
    sent_payload = mock_post.call_args.kwargs["json"]
    assert sent_payload == {"name": "Notebook", "price": 3.5, "stock": 20}

    captured = capsys.readouterr()
    assert "Item created" in captured.out


def test_add_new_item_invalid_price(capsys):
    fake_inputs = ["Notebook", "abc", "20", ""]

    with patch("builtins.input", side_effect=fake_inputs), \
         patch("cli.requests.post") as mock_post:
        cli.add_new_item()

    mock_post.assert_not_called() 
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_delete_item_success(capsys):
    fake_response = Mock()
    fake_response.status_code = 204

    with patch("builtins.input", return_value="1"), \
         patch("cli.requests.delete", return_value=fake_response):
        cli.delete_item()

    captured = capsys.readouterr()
    assert "deleted" in captured.out


def test_delete_item_not_found(capsys):
    fake_response = Mock()
    fake_response.status_code = 404
    fake_response.json.return_value = {"error": "Item 999 not found"}

    with patch("builtins.input", return_value="999"), \
         patch("cli.requests.delete", return_value=fake_response):
        cli.delete_item()

    captured = capsys.readouterr()
    assert "Failed" in captured.out


def test_find_item_on_api_by_barcode(capsys):
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"name": "Nutella", "barcode": "3017620422003"}

    fake_inputs = ["b", "3017620422003"]

    with patch("builtins.input", side_effect=fake_inputs), \
         patch("cli.requests.get", return_value=fake_response):
        cli.find_item_on_api()

    captured = capsys.readouterr()
    assert "Nutella" in captured.out