from flask import Blueprint

inventory_bp = Blueprint("inventory", __name__)


@inventory_bp.route("/")
def home():
    return {
        "message": "Inventory Management API",
        "status": "running"
    }