import json

DATA_FILE = "campus_data.json"

resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
]

fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump({"resources": resources, "borrow_records": borrow_records}, file, indent=4)


def load_data():
    global resources, borrow_records
    try:
        with open(DATA_FILE) as file:
            data = json.load(file)
        resources = data["resources"]
        borrow_records = data["borrow_records"]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        save_data()


def find_resource(resource_id):
    return next(
        (r for r in resources if r["id"].lower() == resource_id.lower()),
        None
    )


def find_record(fellow_id, resource_id):
    return next(
        (
            r for r in borrow_records
            if r["fellow_id"] == fellow_id and r["resource_id"] == resource_id
        ),
        None
    )


def get_quantity(prompt):
    try:
        quantity = int(input(prompt))
        if quantity <= 0:
            print("Error: Quantity must be greater than 0.")
            return None
        return quantity
    except ValueError:
        print("Error: Quantity must be a whole number.")
        return None


def add_resource():
    print("\n========== ADD RESOURCE ==========")

    resource_id = input("Enter resource ID: ").strip()

    if not resource_id:
        print("Error: Resource ID cannot be empty.")
        return

    if find_resource(resource_id):
        print("Error: Resource ID already exists.")
        return

    name = input("Enter resource name: ").strip()
    category = input("Enter resource category: ").strip()

    if not name or not category:
        print("Error: Name and category cannot be empty.")
        return

    try:
        total = int(input("Enter total units: "))
        if total <= 0:
            raise ValueError
    except ValueError:
        print("Error: Total units must be a whole number greater than 0.")
        return

    resources.append({
        "id": resource_id,
        "name": name,
        "category": category,
        "total": total,
        "available": total
    })

    save_data()
    print("Resource added successfully.")


def list_resources():
    print("\n========== RESOURCE INVENTORY ==========")

    if not resources:
        print("No resources available.")
        return

    for r in resources:
        print(
            f"ID: {r['id']} | Name: {r['name']} | "
            f"Category: {r['category']} | "
            f"Total: {r['total']} | Available: {r['available']}"
        )


def borrow_resource(fellow_id=None, resource_id=None, quantity=None, demo=False):
    if not fellow_id:
        fellow_id = input("Enter fellow ID: ").strip().upper()

    if fellow_id not in fellows:
        print("Rejected: Fellow ID not found." if demo else "Error: Fellow ID not found.")
        return False

    if not resource_id:
        resource_id = input("Enter resource ID: ").strip().upper()

    resource = find_resource(resource_id)

    if not resource:
        print("Rejected: Resource ID not found." if demo else "Error: Resource ID not found.")
        return False

    if quantity is None:
        quantity = get_quantity("Enter quantity: ")
        if quantity is None:
            return False

    if quantity > resource["available"]:
        message = f"Rejected: Only {resource['available']} {resource['name']}(s) available."
        if not demo:
            message = f"Error: Not enough units available. Only {resource['available']} available."
        print(message)
        return False

    resource["available"] -= quantity

    record = find_record(fellow_id, resource_id)

    if record:
        record["quantity"] += quantity
    else:
        borrow_records.append({
            "fellow_id": fellow_id,
            "resource_id": resource_id,
            "quantity": quantity
        })

    if not demo:
        save_data()
        print(
            f"Borrowing successful: {fellows[fellow_id]} borrowed "
            f"{quantity} {resource['name']}(s)."
        )
    else:
        print(
            f"Successful: {fellows[fellow_id]} borrowed "
            f"{quantity} {resource['name']}(s)."
        )

    return True


def return_resource(fellow_id=None, resource_id=None, quantity=None, demo=False):
    if not fellow_id:
        fellow_id = input("Enter fellow ID: ").strip().upper()

    if fellow_id not in fellows:
        print("Rejected: Fellow ID not found." if demo else "Error: Fellow ID not found.")
        return False

    if not resource_id:
        resource_id = input("Enter resource ID: ").strip().upper()

    resource = find_resource(resource_id)

    if not resource:
        print("Rejected: Resource ID not found." if demo else "Error: Resource ID not found.")
        return False

    record = find_record(fellow_id, resource_id)

    if not record:
        print(
            "Rejected: No current loan for this resource."
            if demo
            else "Error: This fellow does not have this resource on loan."
        )
        return False

    if quantity is None:
        quantity = get_quantity("Enter quantity to return: ")
        if quantity is None:
            return False

    if quantity > record["quantity"]:
        message = f"Rejected: Cannot return {quantity}. Current loan is {record['quantity']}."
        if not demo:
            message = (
                f"Error: Cannot return {quantity}. "
                f"{fellows[fellow_id]} currently has only "
                f"{record['quantity']} on loan."
            )
        print(message)
        return False

    resource["available"] += quantity
    record["quantity"] -= quantity

    if record["quantity"] == 0:
        borrow_records.remove(record)

    if not demo:
        save_data()
        print(
            f"Return successful: {fellows[fellow_id]} returned "
            f"{quantity} {resource['name']}(s)."
        )
    else:
        print(
            f"Successful: {fellows[fellow_id]} returned "
            f"{quantity} {resource['name']}(s)."
        )

    return True


def search_resources():
    print("\n========== SEARCH RESOURCES ==========")
    term = input("Enter resource name to search: ").strip().lower()

    if not term:
        print("Error: Search term cannot be empty.")
        return

    found = [r for r in resources if term in r["name"].lower()]

    if not found:
        print("No matching resources found.")
        return

    for r in found:
        print(
            f"{r['id']} - {r['name']} - {r['category']} - "
            f"Available: {r['available']}"
        )


def filter_by_category():
    print("\n========== FILTER BY CATEGORY ==========")
    category = input("Enter category: ").strip().lower()

    if not category:
        print("Error: Category cannot be empty.")
        return

    found = [r for r in resources if r["category"].lower() == category]

    if not found:
        print("No resources found in that category.")
        return

    for r in found:
        print(
            f"{r['id']} - {r['name']} - "
            f"Total: {r['total']} - Available: {r['available']}"
        )


def show_reports():
    print("\n========== RESOURCE REPORT ==========")

    total = sum(r["total"] for r in resources)
    available = sum(r["available"] for r in resources)
    borrowed = total - available

    print(f"Total units: {total}")
    print(f"Available units: {available}")
    print(f"Units currently borrowed: {borrowed}")

    low_stock = [r for r in resources if r["available"] < 3]

    print("\nResources with fewer than 3 available units:")

    if low_stock:
        for r in low_stock:
            print(f"- {r['name']} ({r['available']} available)")
    else:
        print("- None")

    borrowed_amounts = [r["total"] - r["available"] for r in resources]
    highest = max(borrowed_amounts, default=0)

    print("\nResource(s) with the most units currently borrowed:")

    if highest == 0:
        print("- None")
    else:
        for r in resources:
            if r["total"] - r["available"] == highest:
                print(f"- {r['name']} ({highest} borrowed)")


def show_borrow_records():
    print("\n========== BORROWING RECORDS ==========")

    if not borrow_records:
        print("No active borrowing records.")
        return

    for record in borrow_records:
        resource = find_resource(record["resource_id"])
        name = resource["name"] if resource else "Unknown Resource"

        print(
            f"Fellow: {fellows.get(record['fellow_id'], 'Unknown')} "
            f"({record['fellow_id']})"
        )
        print(f"Resource: {name} ({record['resource_id']})")
        print(f"Quantity: {record['quantity']}")
        print("-----------------------------")


def run_demonstration():
    global resources, borrow_records

    original_resources = resources
    original_records = borrow_records

    resources = [
        {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
        {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
        {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
    ]
    borrow_records = []

    print("\n========== REQUIRED DEMONSTRATION ==========")

    print("\n1. F001 borrows 2 laptops")
    borrow_resource("F001", "R001", 2, True)

    print("\n2. F002 borrows 3 keyboards")
    borrow_resource("F002", "R002", 3, True)

    print("\n3. F001 returns 1 laptop")
    return_resource("F001", "R001", 1, True)

    print("\n4. F003 requests 4 headsets")
    borrow_resource("F003", "R003", 4, True)

    print("\n5. F002 tries to return 4 keyboards")
    return_resource("F002", "R002", 4, True)

    print("\n6. Search for LAPtop")
    matches = [r for r in resources if "laptop" in r["name"].lower()]
    for r in matches:
        print(f"Found: {r['name']} ({r['id']})")

    print("\n7. Final Report")
    show_reports()

    resources = original_resources
    borrow_records = original_records

    print("\nDemonstration complete. Saved data was not changed.")


def show_menu():
    print("""
=============================================
   CAMPUS RESOURCE MANAGEMENT SYSTEM
=============================================
1. Add resource
2. List resources
3. Borrow resource
4. Return resource
5. Search resources
6. Filter by category
7. Show reports
8. Show borrowing records
9. Run required demonstration
0. Exit
=============================================""")


def main():
    load_data()

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        actions = {
            "1": add_resource,
            "2": list_resources,
            "3": borrow_resource,
            "4": return_resource,
            "5": search_resources,
            "6": filter_by_category,
            "7": show_reports,
            "8": show_borrow_records,
            "9": run_demonstration
        }

        if choice == "0":
            print("Thank you for using the Campus Resource Management System.")
            break

        action = actions.get(choice)

        if action:
            action()
        else:
            print("Error: Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()