inventory = []
_next_id = 1


def reset_inventory():
    global inventory, _next_id
    inventory = []
    _next_id = 1

# returning all my inventory items
def get_all_items():
    return inventory

# return all my inventory items with a specific id
def get_item_by_id(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


def add_item(name, price, stock, barcode=None):
    global _next_id
    item = {
        "id": _next_id,
        "name": name,
        "price": price,
        "stock": stock,
        "barcode": barcode,
    }
    inventory.append(item)
    _next_id += 1
    return item


def update_item(item_id, price=None, stock=None):
    item = get_item_by_id(item_id)
    if item is None:
        return None
    if price is not None:
        item["price"] = price
    if stock is not None:
        item["stock"] = stock
    return item


def delete_item(item_id):
    global inventory
    item = get_item_by_id(item_id)
    if item is None:
        return False
    inventory = [i for i in inventory if i["id"] != item_id]
    return True
