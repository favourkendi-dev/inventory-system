
import pytest
from app import create_app
from app.config import TestingConfig
from app import models

# creates a fresh Flask app configured for testing
@pytest.fixture
def app():
   
    app = create_app(TestingConfig)
    yield app

# creates a test client for the Flask app
@pytest.fixture
def client(app):
    return app.test_client()

# resets the inventory before each test to ensure test isolation
@pytest.fixture(autouse=True)
def reset_inventory_before_each_test():
    models.reset_inventory()
    yield
    models.reset_inventory()