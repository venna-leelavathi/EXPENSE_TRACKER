import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"

# Create CSV file if not exists
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "date", "description", "amount", "category"])


# Generate unique ID
def generate_id():
    return int(datetime.now().timestamp())


# Add Expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: "))
    except:
        print("Amount must be numeric")
        return

    category = input("Enter category: ")
    if category.strip() == "":
        print("Category cannot be empty")
        return

    expense_id = generate_id()

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([expense_id, date, description, amount, category])

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
    search = input("Enter category to search: ").lower()
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
    month = input("Enter month (YYYY-MM): ")
    total = 0

    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["date"].startswith(month):
                total += float(row["amount"])

    print("Total expenses for", month, "=", total)


# Delete by ID
def delete_expense():
    delete_id = input("Enter ID to delete: ")
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