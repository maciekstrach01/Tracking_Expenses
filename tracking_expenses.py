import os
from datetime import datetime
import calendar

expenses_directory = "expenses"
if not os.path.exists(expenses_directory):
    os.makedirs(expenses_directory)

def get_month_filename(month):
    return os.path.join(expenses_directory, f"expenses_{month}.txt")

def load_expenses(month):
    filename = get_month_filename(month)
    expenses = []
    if os.path.exists(filename):
        with open(filename, "r") as file:
            for line in file:
                expense_amount, expense_type, expense_date = line.strip().split(" - ")
                expenses.append((int(expense_amount), expense_type, month, expense_date))
    return expenses

def save_expenses(month, expenses):
    filename = get_month_filename(month)
    with open(filename, "w") as file:
        for expense_amount, expense_type, _, expense_date in expenses:
            file.write(f"{expense_amount} - {expense_type} - {expense_date}\n")

def show_expenses(month):
    expenses = load_expenses(month)
    expenses.sort(reverse=True, key=lambda x: x[0])
    month_name = calendar.month_name[month]
    print(f"\n{month_name.upper()}")

    for expense_amount, expense_type, _, expense_date in expenses:
        print(f'{expense_amount} - {expense_type} - {expense_date}')

def add_expense(month):
    try:
        expenses = load_expenses(month)
        month_name = calendar.month_name[month]
        print(f"\n{month_name.upper()}")

        print()
        while True:
            try:
                expense_amount = int(input("Specify the amount [PLN]: "))
                if expense_amount < 0:
                    raise ValueError("The amount must not be negative.")
                break
            except ValueError:
                print("Enter the correct number.")

        expense_type = input("Specify the type of expense (food, entertainment, home, other):")

        now = datetime.now()
        expense_date = now.strftime("%Y-%m-%d %H:%M:%S")

        expense = (expense_amount, expense_type, month, expense_date)
        expenses.append(expense)
        save_expenses(month, expenses)
        print(f"The expense was added on: {expense_date}")

    except ValueError as ve:
        print(f"Error: {ve}")
        print("Enter the correct number.")

def show_stats(month):
    expenses = load_expenses(month)
    total_amount_this_month = sum(expense_amount for expense_amount, _, _, _ in expenses)
    number_of_expenses_this_month = len(expenses)
    average_expense_this_month = total_amount_this_month / number_of_expenses_this_month

    all_expenses = []
    for i in range(1, 13):
        all_expenses.extend(load_expenses(i))

    total_amount_all = sum(expense_amount for expense_amount, _, _, _ in all_expenses)
    average_expense_all = total_amount_all / len(all_expenses)

    print()
    print("Statistics")
    print("All expenses this month [PLN]:", total_amount_this_month)
    print("Average expenditure this month [PLN]: ", average_expense_this_month)
    print("All expenses [PLN]:", total_amount_all)
    print("Average expenditure [PLN]: ", average_expense_all)

while True:
    print()
    print("Menu:")
    print("1. Select month")
    print("2. Exit the application")
    try:
        main_choice = int(input("Select an option (1 or 2): "))
        if main_choice not in [1, 2]:
            raise ValueError("Select option 1 or 2.")

        if main_choice == 2:
            break

        if main_choice == 1:
            month = None
            while month is None or month not in range(1, 13):
                try:
                    month = int(input("Select the month [1-12]: "))
                    if month not in range(1, 13):
                        print("Select a month between 1 and 12.")
                except ValueError:
                    print("Enter the correct number.")

            month_name = calendar.month_name[month]

            while True:
                print()
                print(f"{month_name.upper()} - Menu:")
                print("0. Return to main menu")
                print("1. View all expenditure")
                print("2. Add expense")
                print("3. Statistics")
                try:
                    choice = int(input("Select the [0-3] option: "))
                    if choice not in range(0, 4):
                        raise ValueError("Select an option from the range 0-3.")

                    if choice == 0:
                        break

                    if choice == 1:
                        show_expenses(month)

                    if choice == 2:
                        add_expense(month)

                    if choice == 3:
                        show_stats(month)

                except ValueError as ve:
                    print(f"Error: {ve}")
                    print("Enter the correct number.")

    except ValueError as ve:
        print(f"Error: {ve}")
        print("Enter the correct number.")
