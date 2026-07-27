from flask import Blueprint, jsonify, request
from marshmallow import ValidationError, EXCLUDE
from app.external_api import find_by_barcode, search_by_name, ExternalAPIError

from app import models
from app.schema import ItemSchema, ItemUpdateSchema 

inventory_bp = Blueprint("inventory", __name__)

item_schema = ItemSchema()
item_update_schema = ItemUpdateSchema()

# Get all inventory items
@inventory_bp.route("/inventory", methods=["GET"])
def get_inventory():
    items = models.get_all_items()
    return jsonify(item_schema.dump(items, many=True)), 200

# Get a single inventory item by ID
@inventory_bp.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = models.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": f"Item {item_id} not found"}), 404
    return jsonify(item_schema.dump(item)), 200

# Create a new inventory item
@inventory_bp.route("/inventory", methods=["POST"])
def create_item():
    json_data = request.get_json(silent=True)
    if json_data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        data = item_schema.load(json_data , unknown=EXCLUDE)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    new_item = models.add_item(
        name=data["name"],
        price=data["price"],
        stock=data["stock"],
        barcode=data.get("barcode"),
    )
    return jsonify(item_schema.dump(new_item)), 201

# Update an existing inventory item
@inventory_bp.route("/inventory/<int:item_id>", methods=["PATCH", "PUT"])
def update_item(item_id):
    json_data = request.get_json(silent=True)
    if json_data is None:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        data = item_update_schema.load(json_data, unknown=EXCLUDE)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    updated = models.update_item(
        item_id,
        price=data.get("price"),
        stock=data.get("stock"),
    )
    if updated is None:
        return jsonify({"error": f"Item {item_id} not found"}), 404

    return jsonify(item_schema.dump(updated)), 200

# Delete an inventory item
@inventory_bp.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    deleted = models.delete_item(item_id)
    if not deleted:
        return jsonify({"error": f"Item {item_id} not found"}), 404
    return "", 204
# Look up a product by barcode or name
@inventory_bp.route("/lookup", methods=["GET"])
def lookup_product():
    barcode = request.args.get("barcode")
    name = request.args.get("name")

    if not barcode and not name:
        return jsonify({"error": "Provide either a 'barcode' or 'name' query parameter"}), 400

    try:
        if barcode:
            result = find_by_barcode(barcode)
            if result is None:
                return jsonify({"error": f"No product found for barcode {barcode}"}), 404
            return jsonify(result), 200
        else:
            results = search_by_name(name)
            return jsonify(results), 200
    except ExternalAPIError as e:
        return jsonify({"error": str(e)}), 502