import requests

BASE_URL = "http://127.0.0.1:5000"


def print_menu():
    print("\nInventory Management CLI Menu:")
    print("1. View all inventory")
    print("2. View item details")
    print("3. Add new item")
    print("4. Update item price or stock")
    print("5. Delete item")
    print("6. Find item on OpenFoodFacts")
    print("0. Exit")


def view_all_items():
    response = requests.get(f"{BASE_URL}/inventory")
    items = response.json()
    if not items:
        print("Inventory is empty.")
        return
    for item in items:
        print(f"  [{item['id']}] {item['name']} — ${item['price']} — stock: {item['stock']} — barcode: {item.get('barcode')}")


def view_item_details():
    item_id = input("Enter item ID: ").strip()
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 404:
        print(f"Item {item_id} not found.")
        return
    print(response.json())


def add_new_item():
    name = input("Name: ").strip()
    price_input = input("Price: ").strip()
    stock_input = input("Stock: ").strip()
    barcode = input("Barcode (optional, press Enter to skip): ").strip() or None

    # server still validates for real
    try:
        price = float(price_input)
        stock = int(stock_input)
    except ValueError:
        print("Error: price must be a number and stock must be a whole number.")
        return

    payload = {"name": name, "price": price, "stock": stock}
    if barcode:
        payload["barcode"] = barcode

    response = requests.post(f"{BASE_URL}/inventory", json=payload)
    if response.status_code == 201:
        print("Item created:", response.json())
    else:
        print(f"Failed ({response.status_code}):", response.json())


def update_item():
    item_id = input("Enter item ID to update: ").strip()
    price_input = input("New price (press Enter to skip): ").strip()
    stock_input = input("New stock (press Enter to skip): ").strip()

    payload = {}
    if price_input:
        try:
            payload["price"] = float(price_input)
        except ValueError:
            print("Error: price must be a number.")
            return
    if stock_input:
        try:
            payload["stock"] = int(stock_input)
        except ValueError:
            print("Error: stock must be a whole number.")
            return

    if not payload:
        print("Nothing to update.")
        return

    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
    if response.status_code == 200:
        print("Item updated:", response.json())
    else:
        print(f"Failed ({response.status_code}):", response.json())


def delete_item():
    item_id = input("Enter item ID to delete: ").strip()
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 204:
        print(f"Item {item_id} deleted.")
    else:
        print(f"Failed ({response.status_code}):", response.json())


def find_item_on_api():
    choice = input("Search by (b)arcode or (n)ame? ").strip().lower()
    if choice == "b":
        barcode = input("Barcode: ").strip()
        response = requests.get(f"{BASE_URL}/lookup", params={"barcode": barcode})
    elif choice == "n":
        name = input("Name: ").strip()
        response = requests.get(f"{BASE_URL}/lookup", params={"name": name})
    else:
        print("Invalid choice.")
        return

    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Lookup failed ({response.status_code}):", response.json())


def main():
    actions = {
        "1": view_all_items,
        "2": view_item_details,
        "3": add_new_item,
        "4": update_item,
        "5": delete_item,
        "6": find_item_on_api,
    }

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid option, try again.")
            continue
        try:
            action()
        except requests.ConnectionError:
            print("Error: could not reach the API server. Is it running?")


if __name__ == "__main__":
    main()