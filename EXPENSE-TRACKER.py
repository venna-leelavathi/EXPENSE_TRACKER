import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"


def initialize_file():
    """Create CSV file with headers if it does not already exist."""
    if not os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "date", "description", "amount", "category"])
        except OSError as e:
            print(f"Error: Unable to create expenses file: {e}")
            raise SystemExit(1)


def generate_id():
    """Generate a unique ID based on the current timestamp."""
    return int(datetime.now().timestamp())


def add_expense():
    """Prompt the user for expense details, validate, and append to CSV."""
    date = input("Enter date (YYYY-MM-DD): ")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    description = input("Enter description: ")
    if description.strip() == "":
        print("Error: Description cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Error: Amount must be a valid number.")
        return

    if amount <= 0:
        print("Error: Amount must be a positive number.")
        return

    category = input("Enter category: ")
    if category.strip() == "":
        print("Error: Category cannot be empty.")
        return

    expense_id = generate_id()

    try:
        with open(FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([expense_id, date, description, amount, category])
    except OSError as e:
        print(f"Error: Unable to save expense: {e}")
        return

    print("Expense added successfully")


def view_expenses():
    """Display all expenses from the CSV file with totals."""
    total = 0
    count = 0

    print("\nID | Date | Description | Amount | Category")
    print("-" * 50)

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    amount = float(row["amount"])
                except (ValueError, KeyError):
                    print(f"Warning: Skipping malformed row (bad amount): {row}")
                    continue
                print(row["id"], row["date"], row["description"], row["amount"], row["category"])
                total += amount
                count += 1
    except FileNotFoundError:
        print("Error: Expenses file not found. Please add an expense first.")
        return
    except OSError as e:
        print(f"Error: Unable to read expenses file: {e}")
        return

    print("-" * 50)
    print("Total Expenses:", count)
    print("Total Amount:", total)


def search_category():
    """Search and display expenses matching a given category."""
    search = input("Enter category to search: ").strip()
    if search == "":
        print("Error: Category cannot be empty.")
        return

    search_lower = search.lower()
    subtotal = 0
    found = False

    print("\nResults:\n")

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["category"].lower() == search_lower:
                    try:
                        amount = float(row["amount"])
                    except (ValueError, KeyError):
                        print(f"Warning: Skipping malformed row (bad amount): {row}")
                        continue
                    print(row["id"], row["date"], row["description"], row["amount"], row["category"])
                    subtotal += amount
                    found = True
    except FileNotFoundError:
        print("Error: Expenses file not found. Please add an expense first.")
        return
    except OSError as e:
        print(f"Error: Unable to read expenses file: {e}")
        return

    if not found:
        print(f"No expenses found for category: {search}")
    else:
        print("Subtotal for category:", subtotal)


def monthly_total():
    """Calculate and display total expenses for a given month."""
    month = input("Enter month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month, "%Y-%m")
    except ValueError:
        print("Error: Invalid month format. Please use YYYY-MM.")
        return

    total = 0
    found = False

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["date"].startswith(month):
                    try:
                        total += float(row["amount"])
                        found = True
                    except (ValueError, KeyError):
                        print(f"Warning: Skipping malformed row (bad amount): {row}")
                        continue
    except FileNotFoundError:
        print("Error: Expenses file not found. Please add an expense first.")
        return
    except OSError as e:
        print(f"Error: Unable to read expenses file: {e}")
        return

    if not found:
        print(f"No expenses found for month: {month}")
    else:
        print("Total expenses for", month, "=", total)


def delete_expense():
    """Delete an expense record by its ID."""
    delete_id = input("Enter ID to delete: ").strip()
    if delete_id == "":
        print("Error: ID cannot be empty.")
        return

    rows = []
    found = False

    try:
        with open(FILE_NAME, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["id"] != delete_id:
                    rows.append(row)
                else:
                    found = True
    except FileNotFoundError:
        print("Error: Expenses file not found. Please add an expense first.")
        return
    except OSError as e:
        print(f"Error: Unable to read expenses file: {e}")
        return

    if not found:
        print(f"Error: Expense with ID '{delete_id}' not found.")
        return

    try:
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "date", "description", "amount", "category"])
            writer.writeheader()
            writer.writerows(rows)
    except OSError as e:
        print(f"Error: Unable to update expenses file: {e}")
        return

    print("Expense deleted successfully")


def run():
    """Main menu loop for the expense tracker."""
    initialize_file()

    while True:
        print("\n------ Expense Tracker ------")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search by Category")
        print("4. Monthly Total")
        print("5. Delete by ID")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

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
            print("Error: Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    run()