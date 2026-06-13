from utils import (
    initialize_file,
    generate_id,
    read_expenses,
    write_expenses,
    append_expense,
    print_expense_table,
    calculate_total,
    format_expense,
)


# Add Expense
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    description = input("Enter description: ")

    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Amount must be numeric")
        return

    category = input("Enter category: ")
    if category.strip() == "":
        print("Category cannot be empty")
        return

    expense_id = generate_id()
    append_expense([expense_id, date, description, amount, category])
    print("Expense added successfully")


# View All Expenses
def view_expenses():
    expenses = read_expenses()
    print_expense_table(expenses)
    print("Total Expenses:", len(expenses))
    print("Total Amount:", calculate_total(expenses))


# Search by Category
def search_category():
    search = input("Enter category to search: ").lower()
    expenses = read_expenses()
    matched = [row for row in expenses if row["category"].lower() == search]

    print("\nResults:\n")
    for row in matched:
        print(format_expense(row))
    print("Subtotal for category:", calculate_total(matched))


# Monthly Total
def monthly_total():
    month = input("Enter month (YYYY-MM): ")
    expenses = read_expenses()
    matched = [row for row in expenses if row["date"].startswith(month)]
    print("Total expenses for", month, "=", calculate_total(matched))


# Delete by ID
def delete_expense():
    delete_id = input("Enter ID to delete: ")
    expenses = read_expenses()
    remaining = [row for row in expenses if row["id"] != delete_id]

    if len(remaining) == len(expenses):
        print("ID not found")
        return

    write_expenses(remaining)
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
