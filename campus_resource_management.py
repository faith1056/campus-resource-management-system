import json


# ============================================================
# CAMPUS RESOURCE MANAGEMENT SYSTEM
# ============================================================

DATA_FILE = "campus_data.json"


# ============================================================
# STARTING DATA
# ============================================================

default_resources = [
    {
        "id": "R001",
        "name": "Laptop",
        "category": "Electronics",
        "total": 10,
        "available": 10
    },
    {
        "id": "R002",
        "name": "Keyboard",
        "category": "Accessories",
        "total": 5,
        "available": 5
    },
    {
        "id": "R003",
        "name": "Headset",
        "category": "Accessories",
        "total": 3,
        "available": 3
    }
]

resources = default_resources.copy()

fellows = {
    "F001": "Ada",
    "F002": "John",
    "F003": "Grace"
}

borrow_records = []


# ============================================================
# SAVE AND LOAD DATA
# ============================================================

def save_data():
    data = {
        "resources": resources,
        "borrow_records": borrow_records
    }

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    global resources, borrow_records

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        resources = data["resources"]
        borrow_records = data["borrow_records"]

        print("Saved data loaded successfully.")

    except FileNotFoundError:
        print("No saved data found. Starting with default data.")


# ============================================================
# FIND RESOURCE
# ============================================================

def find_resource(resource_id):
    for resource in resources:
        if resource["id"].upper() == resource_id.upper():
            return resource

    return None


# ============================================================
# ADD RESOURCE
# ============================================================

def add_resource():
    print("\n========== ADD RESOURCE ==========")

    resource_id = input("Enter resource ID: ").strip()

    if not resource_id:
        print("Error: Resource ID cannot be empty.")
        return

    if find_resource(resource_id) is not None:
        print("Error: Resource ID already exists.")
        return

    name = input("Enter resource name: ").strip()

    if not name:
        print("Error: Resource name cannot be empty.")
        return

    category = input("Enter resource category: ").strip()

    if not category:
        print("Error: Category cannot be empty.")
        return

    try:
        total = int(input("Enter total units: "))
    except ValueError:
        print("Error: Total units must be a whole number.")
        return

    if total <= 0:
        print("Error: Total units must be greater than 0.")
        return

    resource = {
        "id": resource_id,
        "name": name,
        "category": category,
        "total": total,
        "available": total
    }

    resources.append(resource)

    save_data()

    print("Resource added successfully.")


# ============================================================
# LIST RESOURCES
# ============================================================

def list_resources():
    print("\n========== RESOURCE INVENTORY ==========")

    if not resources:
        print("No resources available.")
        return

    for resource in resources:
        print(f"ID: {resource['id']}")
        print(f"Name: {resource['name']}")
        print(f"Category: {resource['category']}")
        print(f"Total Units: {resource['total']}")
        print(f"Available Units: {resource['available']}")
        print("-----------------------------")


# ============================================================
# BORROW RESOURCE
# ============================================================

def borrow_resource():
    print("\n========== BORROW RESOURCE ==========")

    fellow_id = input("Enter fellow ID: ").strip().upper()

    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return

    resource_id = input("Enter resource ID: ").strip().upper()

    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource ID not found.")
        return

    try:
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Error: Quantity must be a whole number.")
        return

    if quantity <= 0:
        print("Error: Quantity must be greater than 0.")
        return

    if quantity > resource["available"]:
        print(
            f"Error: Not enough units available. "
            f"Only {resource['available']} available."
        )
        return

    # Update stock only after all validation passes
    resource["available"] -= quantity

    existing_record = None

    for record in borrow_records:
        if (
            record["fellow_id"] == fellow_id
            and record["resource_id"] == resource_id
        ):
            existing_record = record
            break

    if existing_record:
        existing_record["quantity"] += quantity
    else:
        borrow_records.append({
            "fellow_id": fellow_id,
            "resource_id": resource_id,
            "quantity": quantity
        })

    save_data()

    print(
        f"Borrowing successful: {fellows[fellow_id]} borrowed "
        f"{quantity} {resource['name']}(s)."
    )


# ============================================================
# RETURN RESOURCE
# ============================================================

def return_resource():
    print("\n========== RETURN RESOURCE ==========")

    fellow_id = input("Enter fellow ID: ").strip().upper()

    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return

    resource_id = input("Enter resource ID: ").strip().upper()

    resource = find_resource(resource_id)

    if resource is None:
        print("Error: Resource ID not found.")
        return

    try:
        quantity = int(input("Enter quantity to return: "))
    except ValueError:
        print("Error: Quantity must be a whole number.")
        return

    if quantity <= 0:
        print("Error: Quantity must be greater than 0.")
        return

    record = None

    for borrow in borrow_records:
        if (
            borrow["fellow_id"] == fellow_id
            and borrow["resource_id"] == resource_id
        ):
            record = borrow
            break

    if record is None:
        print(
            "Error: This fellow does not have "
            "this resource on loan."
        )
        return

    if quantity > record["quantity"]:
        print(
            f"Error: Cannot return {quantity}. "
            f"{fellows[fellow_id]} currently has only "
            f"{record['quantity']} on loan."
        )
        return

    resource["available"] += quantity
    record["quantity"] -= quantity

    if record["quantity"] == 0:
        borrow_records.remove(record)

    save_data()

    print(
        f"Return successful: {fellows[fellow_id]} returned "
        f"{quantity} {resource['name']}(s)."
    )


# ============================================================
# SEARCH RESOURCES
# ============================================================

def search_resources():
    print("\n========== SEARCH RESOURCES ==========")

    search_term = input(
        "Enter resource name to search: "
    ).strip().lower()

    if not search_term:
        print("Error: Search term cannot be empty.")
        return

    found = False

    for resource in resources:
        if search_term in resource["name"].lower():
            print(
                f"{resource['id']} - "
                f"{resource['name']} - "
                f"{resource['category']} - "
                f"Available: {resource['available']}"
            )

            found = True

    if not found:
        print("No matching resources found.")


# ============================================================
# FILTER BY CATEGORY
# ============================================================

def filter_by_category():
    print("\n========== FILTER BY CATEGORY ==========")

    category = input("Enter category: ").strip().lower()

    if not category:
        print("Error: Category cannot be empty.")
        return

    found = False

    for resource in resources:
        if resource["category"].lower() == category:
            print(
                f"{resource['id']} - "
                f"{resource['name']} - "
                f"Total: {resource['total']} - "
                f"Available: {resource['available']}"
            )

            found = True

    if not found:
        print("No resources found in that category.")


# ============================================================
# REPORTS
# ============================================================

def show_reports():
    print("\n========== RESOURCE REPORT ==========")

    total_units = 0
    available_units = 0

    for resource in resources:
        total_units += resource["total"]
        available_units += resource["available"]

    borrowed_units = total_units - available_units

    print(f"Total units: {total_units}")
    print(f"Available units: {available_units}")
    print(f"Units currently borrowed: {borrowed_units}")

    # --------------------------------------------------------
    # LOW STOCK
    # --------------------------------------------------------

    print("\nResources with fewer than 3 available units:")

    low_stock_found = False

    for resource in resources:
        if resource["available"] < 3:
            print(
                f"- {resource['name']} "
                f"({resource['available']} available)"
            )

            low_stock_found = True

    if not low_stock_found:
        print("- None")

    # --------------------------------------------------------
    # MOST BORROWED
    # --------------------------------------------------------

    borrowed_by_resource = {}

    for resource in resources:
        borrowed_by_resource[resource["id"]] = (
            resource["total"] - resource["available"]
        )

    highest_borrowed = max(
        borrowed_by_resource.values(),
        default=0
    )

    print(
        "\nResource(s) with the most "
        "units currently borrowed:"
    )

    if highest_borrowed == 0:
        print("- None")
    else:
        for resource in resources:
            if (
                borrowed_by_resource[resource["id"]]
                == highest_borrowed
            ):
                print(
                    f"- {resource['name']} "
                    f"({highest_borrowed} borrowed)"
                )


# ============================================================
# VIEW BORROWING RECORDS
# ============================================================

def show_borrow_records():
    print("\n========== BORROWING RECORDS ==========")

    if not borrow_records:
        print("No active borrowing records.")
        return

    for record in borrow_records:
        fellow_name = fellows[record["fellow_id"]]

        resource = find_resource(record["resource_id"])

        if resource:
            resource_name = resource["name"]
        else:
            resource_name = "Unknown Resource"

        print(
            f"Fellow: {fellow_name} "
            f"({record['fellow_id']})"
        )

        print(
            f"Resource: {resource_name} "
            f"({record['resource_id']})"
        )

        print(f"Quantity: {record['quantity']}")
        print("-----------------------------")


# ============================================================
# REQUIRED DEMONSTRATION
# ============================================================

def demo_borrow(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Rejected: Fellow ID not found.")
        return

    resource = find_resource(resource_id)

    if resource is None:
        print("Rejected: Resource ID not found.")
        return

    if quantity <= 0:
        print("Rejected: Quantity must be positive.")
        return

    if quantity > resource["available"]:
        print(
            f"Rejected: Only {resource['available']} "
            f"{resource['name']}(s) available."
        )
        return

    resource["available"] -= quantity

    existing_record = None

    for record in borrow_records:
        if (
            record["fellow_id"] == fellow_id
            and record["resource_id"] == resource_id
        ):
            existing_record = record
            break

    if existing_record:
        existing_record["quantity"] += quantity
    else:
        borrow_records.append({
            "fellow_id": fellow_id,
            "resource_id": resource_id,
            "quantity": quantity
        })

    print(
        f"Successful: {fellows[fellow_id]} borrowed "
        f"{quantity} {resource['name']}(s)."
    )


def demo_return(fellow_id, resource_id, quantity):
    if fellow_id not in fellows:
        print("Rejected: Fellow ID not found.")
        return

    resource = find_resource(resource_id)

    if resource is None:
        print("Rejected: Resource ID not found.")
        return

    record = None

    for borrow in borrow_records:
        if (
            borrow["fellow_id"] == fellow_id
            and borrow["resource_id"] == resource_id
        ):
            record = borrow
            break

    if record is None:
        print("Rejected: No current loan for this resource.")
        return

    if quantity <= 0:
        print("Rejected: Quantity must be positive.")
        return

    if quantity > record["quantity"]:
        print(
            f"Rejected: Cannot return {quantity}. "
            f"Current loan is {record['quantity']}."
        )
        return

    resource["available"] += quantity
    record["quantity"] -= quantity

    if record["quantity"] == 0:
        borrow_records.remove(record)

    print(
        f"Successful: {fellows[fellow_id]} returned "
        f"{quantity} {resource['name']}(s)."
    )


def demo_search(search_term):
    found = False

    for resource in resources:
        if search_term.lower() in resource["name"].lower():
            print(
                f"Found: {resource['name']} "
                f"({resource['id']})"
            )

            found = True

    if not found:
        print("No matching resources found.")


def run_demonstration():
    global resources, borrow_records

    print("\n")
    print("=" * 55)
    print("REQUIRED ASSESSMENT DEMONSTRATION")
    print("=" * 55)

    # Save the user's real data temporarily
    original_resources = resources
    original_borrow_records = borrow_records

    # Start demonstration with clean assessment data
    resources = [
        {
            "id": "R001",
            "name": "Laptop",
            "category": "Electronics",
            "total": 10,
            "available": 10
        },
        {
            "id": "R002",
            "name": "Keyboard",
            "category": "Accessories",
            "total": 5,
            "available": 5
        },
        {
            "id": "R003",
            "name": "Headset",
            "category": "Accessories",
            "total": 3,
            "available": 3
        }
    ]

    borrow_records = []

    print("\n1. F001 borrows 2 laptops")
    demo_borrow("F001", "R001", 2)

    print("\n2. F002 borrows 3 keyboards")
    demo_borrow("F002", "R002", 3)

    print("\n3. F001 returns 1 laptop")
    demo_return("F001", "R001", 1)

    print("\n4. F003 requests 4 headsets")
    demo_borrow("F003", "R003", 4)

    print("\n5. F002 tries to return 4 keyboards")
    demo_return("F002", "R002", 4)

    print("\n6. Search for LAPtop")
    demo_search("LAPtop")

    print("\n7. Final Report")
    show_reports()

    # Restore the user's real data
    resources = original_resources
    borrow_records = original_borrow_records

    print("\nDemonstration complete.")
    print("Your saved inventory and borrowing records were not changed.")


# ============================================================
# MENU
# ============================================================

def show_menu():
    print("\n")
    print("=" * 45)
    print(" CAMPUS RESOURCE MANAGEMENT SYSTEM")
    print("=" * 45)

    print("1. Add resource")
    print("2. List resources")
    print("3. Borrow resource")
    print("4. Return resource")
    print("5. Search resources")
    print("6. Filter by category")
    print("7. Show reports")
    print("8. Show borrowing records")
    print("9. Run required demonstration")
    print("0. Exit")

    print("=" * 45)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():
    load_data()

    while True:
        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_resource()

        elif choice == "2":
            list_resources()

        elif choice == "3":
            borrow_resource()

        elif choice == "4":
            return_resource()

        elif choice == "5":
            search_resources()

        elif choice == "6":
            filter_by_category()

        elif choice == "7":
            show_reports()

        elif choice == "8":
            show_borrow_records()

        elif choice == "9":
            run_demonstration()

        elif choice == "0":
            print(
                "Thank you for using the "
                "Campus Resource Management System."
            )
            break

        else:
            print(
                "Error: Invalid choice. "
                "Please select a valid option."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()