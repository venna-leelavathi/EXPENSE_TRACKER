# EXPENSE_TRACKER
Expense Tracker by using Python Programming

EXPENSE TRACKER :– 

 Description:
 ==============
The Menu-Driven Expense Tracker is a Python console application used to record and manage daily expenses. The program stores all expense details in a CSV file (expenses.csv) so that the data is saved permanently and can be accessed later.
This application allows users to interact through a menu-based interface, where they can choose different options such as adding expenses, viewing all expenses, searching by category, calculating monthly totals, deleting records, and exiting the program.
1. CSV Data Model
The program stores data in a CSV file named expenses.csv with the following columns:
id – Unique ID generated automatically using a timestamp
date – Date of the expense in YYYY-MM-DD format
description – Short description of the expense
amount – Expense amount entered by the user
category – Type of expense (Food, Transport, Shopping, etc.)
Example:
Copy code

id,date,description,amount,category
1710001111,2026-03-14,Lunch,120,Food
1710001211,2026-03-14,Bus Ticket,50,Transport
If the CSV file does not exist, the program automatically creates the file and adds the header row.
2. Menu System
The program runs inside a loop-based menu system, allowing users to repeatedly choose operations until they exit.
Menu Options:
Add Expense
View All Expenses
Search by Category
Monthly Total
Delete by ID
Exit
This menu improves user interaction and program structure.
3. Features of the Program
Add Expense
This option allows the user to add a new expense.
The program asks for:
Date
Description
Amount
Category
Validation is performed:
The amount must be numeric.
The category cannot be empty.
A unique ID is automatically generated and the expense is saved to the CSV file.
View All Expenses
This option displays all stored expenses in a table-like format.
It also shows:
Total number of expenses
Total amount spent
This helps the user quickly understand their spending.
Search by Category
This option allows the user to search expenses based on a specific category.
Example categories:
Food
Transport
Shopping
Entertainment
The search is case-insensitive, meaning "food" and "Food" will both work.
The program also calculates and displays the subtotal for that category.
Monthly Total
This feature calculates the total expenses for a specific month.
The user enters the month in the format:
Copy code

YYYY-MM
Example:
Copy code

2026-03
The program then adds all expenses that belong to that month and displays the total monthly spending.
Delete by ID
This option allows the user to delete a specific expense record.
Steps:
The user enters the expense ID.
The program searches for that ID in the CSV file.
If found, the record is removed.
The CSV file is rewritten without that record.
If the ID does not exist, the program displays "ID not found".
Exit
This option stops the program and exits the menu loop.
4. Code Structure
The program follows good programming practices by dividing tasks into functions:
initialize_file() → Creates CSV file if it doesn't exist
generate_id() → Generates unique ID
add_expense() → Adds new expense
view_expenses() → Displays all expenses
search_category() → Filters expenses by category
monthly_total() → Calculates monthly expenses
delete_expense() → Deletes expense by ID
run() → Controls the menu system
This modular design makes the program easier to understand, maintain, and expand.
5. Importance of This Task
This project helps in learning important programming concepts such as:
File handling (CSV)
Menu-driven CLI applications
Data validation
Searching and filtering data
Aggregating totals
Modular programming using functions
These skills are very useful for automation scripts, backend development, and data processing tasks.
