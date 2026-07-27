# Inventory Management System

A Flask-based inventory management system with OpenFoodFacts API integration

## Features

- **Full CRUD Operations** — Create, Read, Update, Delete inventory items
- **OpenFoodFacts Integration** — Search products and retrieve product information from external API
- **REST API Backend** — Flask-based inventory management API
- **Command Line Interface (CLI)** — Manage inventory from terminal
- **Data Validation** — Request validation using Marshmallow schemas
- **Error Handling** — Handles invalid requests, missing items, and API failures
- **Automated Testing** — pytest-based test suite

## Installation & Setup

### Prerequisites
- Python 3.10+
- pipenv

### Clone the Repository

```bash
git clone https://github.com/favourkendi-dev/inventory_project.git
cd inventory_project
```

### Install Dependencies

```bash
pipenv install
```

### Activate Virtual Environment

```bash
pipenv shell
```

### Run the Flask App

```bash
pipenv run flask run
```

The application will be available at:

```
http://127.0.0.1:5000/
```

### Run CLI (Optional)

In a new terminal:

```bash
pipenv run python cli.py
```

---

## Request/Response Examples

### Add Item (POST /inventory)

```json
// Request
{
  "name": "Rice",
  "price": 200.00,
  "stock": 10,
  "barcode": "123456789"
}

// Response
{
  "id": 1,
  "name": "Rice",
  "price": 200.00,
  "stock": 10,
  "barcode": "123456789"
}
```

### Get All Items (GET /inventory)

```json
// Response
[
  {
    "id": 1,
    "name": "Rice",
    "price": 200.00,
    "stock": 10,
    "barcode": "123456789"
  }
]
```

### Get Single Item (GET /inventory/<id>)

```json
// Response
{
  "id": 1,
  "name": "Rice",
  "price": 200.00,
  "stock": 10,
  "barcode": "123456789"
}
```

### Update Item (PATCH /inventory/<id>)

```json
// Request
{
  "price": 250.00,
  "stock": 15
}

// Response
{
  "id": 1,
  "name": "Rice",
  "price": 250.00,
  "stock": 15,
  "barcode": "123456789"
}
```

### Delete Item (DELETE /inventory/<id>)

Response:

```
204 No Content
```

---

## OpenFoodFacts Integration Examples

### Search Product By Barcode (GET /lookup?barcode=3017624010701)

```json
// Response
{
  "name": "Nutella",
  "barcode": "3017624010701",
  "brands": "Ferrero",
  "categories": "Spreads"
}
```

### Search Product By Name (GET /lookup?name=nutella)

```json
// Response
[
  {
    "name": "Nutella",
    "barcode": "3017624010701",
    "brands": "Ferrero",
    "categories": "Spreads"
  }
]
```

---

## CLI Usage Examples

The CLI tool allows you to manage inventory directly from the terminal.

### Start the CLI

```bash
pipenv run python cli.py
```

### Menu Options

```
 Inventory Management CLI 

1. View all inventory
2. View item details
3. Add new item
4. Update item price/stock
5. Delete item
6. Find item on OpenFoodFacts
0. Exit
```

### Example 1: View All Items

```
Choose an option: 1

Current Inventory

[1] Rice — $200 — stock: 10 — barcode: 123456789
[2] Sugar — $150 — stock: 5 — barcode: 987654321
```

### Example 2: Add New Item

```
Choose an option: 3

Name: Milk
Price: 120
Stock: 12
Barcode: 123456789

Item created successfully
```

### Example 3: Search OpenFoodFacts

```
Choose an option: 6

Search by (b)arcode or (n)ame? n

Name: nutella

Found:
Nutella
Brand: Ferrero
Category: Spreads
```

### Example 4: Update Item

```
Choose an option: 4

Enter item ID to update: 1

New price: 250
New stock: 15

Item updated successfully
```

### Example 5: Delete Item

```
Choose an option: 5

Enter item ID to delete: 2

Item deleted successfully
```

---

## Project Structure

```
inventory_project/
├── app/
│   ├── __init__.py              # Flask application factory
│   ├── routes.py                # API routes
│   ├── models.py                # Inventory data operations
│   ├── schema.py                # Marshmallow validation schemas
│   └── external_api.py          # OpenFoodFacts API integration
│
├── cli.py                        # Command line interface
├── Pipfile                       # Pipenv dependencies
├── Pipfile.lock                  # Locked dependencies
├── pytest.ini                    # Pytest configuration
├── README.md                     # Documentation
│
└── tests/
    └── test_app.py               # Application tests
```

---

## Technologies Used

- Python 3.12 — Backend language
- Flask — Web framework
- Marshmallow — Data validation
- Requests — HTTP client for API calls
- OpenFoodFacts API — External product data
- Pipenv — Virtual environment management
- pytest — Testing framework
- unittest.mock — Mocking for tests

---

## Testing

Run the test suite:

```bash
pipenv run pytest tests/ -v
```

Check coverage:

```bash
pipenv run pytest tests/ --cov=app
```

---

## Debug Tools

- Flask Debug Mode — Used during development
- Postman — Used to test API endpoints manually
- pytest — Automated testing framework
- Git/GitHub — Version control

---

## Author

Favour Kendi