import csv
import os
import stat
from datetime import datetime

FILE_NAME = "expenses.csv"
MAX_INPUT_LENGTH = 200

def sanitize_csv_field(value):
    """Prevent CSV injection by escaping formula-trigger characters."""
    if value and value[0] in ('=', '+', '-', '@', '\t', '\r'):
        return "'" + value
    return value


def validate_date(date_str):
    """Validate date is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# Create CSV file if not exists
def initialize_file():
    if not os.path.exists(FILE_NAME):
        fd = os.open(FILE_NAME, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "date", "description", "amount", "category"])
    else:
        os.chmod(FILE_NAME, stat.S_IRUSR | stat.S_IWUSR)


# Generate unique ID
def generate_id():
    return int(datetime.now().timestamp())


# Add Expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")[:MAX_INPUT_LENGTH]
    if not validate_date(date):
        print("Invalid date format. Use YYYY-MM-DD")
        return

    description = input("Enter description: ")[:MAX_INPUT_LENGTH]
    if description.strip() == "":
        print("Description cannot be empty")
        return

    try:
        amount = float(input("Enter amount: ")[:MAX_INPUT_LENGTH])
    except ValueError:
        print("Amount must be numeric")
        return

    if amount <= 0:
        print("Amount must be a positive number")
        return

    category = input("Enter category: ")[:MAX_INPUT_LENGTH]
    if category.strip() == "":
        print("Category cannot be empty")
        return

    expense_id = generate_id()
    safe_description = sanitize_csv_field(description.strip())
    safe_category = sanitize_csv_field(category.strip())

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([expense_id, date, safe_description, amount, safe_category])

    print("Expense added successfully")


# View All Expenses
def view_expenses():
    total = 0
    count = 0

    print("\nID | Date | Description | Amount | Category")
    print("-"*50)

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row["id"], row["date"], row["description"], row["amount"], row["category"])
            total += float(row["amount"])
            count += 1

    print("-"*50)
    print("Total Expenses:", count)
    print("Total Amount:", total)


# Search by Category
def search_category():
    search = input("Enter category to search: ")[:MAX_INPUT_LENGTH].lower()
    subtotal = 0

    print("\nResults:\n")

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["category"].lower() == search:
                print(row["id"], row["date"], row["description"], row["amount"], row["category"])
                subtotal += float(row["amount"])

    print("Subtotal for category:", subtotal)


# Monthly Total
def monthly_total():
    month = input("Enter month (YYYY-MM): ")[:MAX_INPUT_LENGTH].strip()

    try:
        datetime.strptime(month + "-01", "%Y-%m-%d")
    except ValueError:
        print("Invalid month format. Use YYYY-MM")
        return

    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"].startswith(month):
                total += float(row["amount"])

    print("Total expenses for", month, "=", total)


# Delete by ID
def delete_expense():
    delete_id = input("Enter ID to delete: ")[:MAX_INPUT_LENGTH].strip()
    rows = []
    found = False

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["id"] != delete_id:
                rows.append(row)
            else:
                found = True

    if not found:
        print("ID not found")
        return

    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["id","date","description","amount","category"])
        writer.writeheader()
        writer.writerows(rows)

    print("Expense deleted successfully")


# Menu Loop
def run():
    initialize_file()

    while True:
        print("\n------ Expense Tracker ------")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search by Category")
        print("4. Monthly Total")
        print("5. Delete by ID")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_category()
        elif choice == "4":
            monthly_total()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            print("Exiting program")
            break
        else:
            print("Invalid choice")


# Run Program
run()