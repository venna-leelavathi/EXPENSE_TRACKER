import csv
import os
from datetime import datetime

FILE_NAME = "expenses.csv"
FIELDNAMES = ["id", "date", "description", "amount", "category"]


def initialize_file():
    """Create CSV file with header if it does not exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDNAMES)


def generate_id():
    """Generate a unique ID based on current timestamp."""
    return int(datetime.now().timestamp())


def read_expenses():
    """Read all expenses from the CSV file and return as list of dicts."""
    expenses = []
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expenses.append(row)
    return expenses


def write_expenses(rows):
    """Write a list of expense dicts to the CSV file (overwrites)."""
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def append_expense(expense_row):
    """Append a single expense row to the CSV file."""
    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(expense_row)


def format_expense(row):
    """Format a single expense row as a display string."""
    return f"{row['id']} | {row['date']} | {row['description']} | {row['amount']} | {row['category']}"


def print_expense_table(rows):
    """Print a list of expense rows in table format with header and totals."""
    print("\nID | Date | Description | Amount | Category")
    print("-" * 50)
    for row in rows:
        print(format_expense(row))
    print("-" * 50)


def calculate_total(rows):
    """Calculate the sum of amounts from a list of expense rows."""
    return sum(float(row["amount"]) for row in rows)
