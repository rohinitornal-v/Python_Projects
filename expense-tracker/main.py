"""
main.py - CLI Entry Point
Handles all user interaction for the Expense Tracker.
This is the only file that prints to the screen and reads user input.

This is the CLI logic - completely separate from core logic.
All business logic lives in app/expense_manager.py
"""

from app.expense_manager import (
    add_expense,
    get_all_expenses,
    filter_by_category,
    get_total,
    delete_expense,
    get_total,
)
from app.validator import ValidationError


# ----------------------------
# Display Functions
# ----------------------------
def display_menu():
    """Display the main menu options to the user."""
    print("\nExpense Tracker Menu:")
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Filter Expenses by Category")
    print("4. View Total Expenses")
    print("5. Delete Expense")
    print("6. Exit")


def display_expenses(expenses):
    """Display a list of expenses in a formatted way."""
    if not expenses:
        print("No expenses found.")
        return
    print("\nExpenses:")

    # enumerate(expenses, 1) gives 1-based index

    for idx, expense in enumerate(expenses, start=1):
        print(
            f"{idx}. {expense['title']} - ${expense['amount']:.2f} ({expense['category']})"
        )


# ──────────────────────────────────────────
# Menu Action Functions
# ──────────────────────────────────────────


def handle_add_expense():
    """Handle adding a new expense."""
    print("\n--- Add Expense ---")
    title = input("Enter expense title: ").strip()
    amount = input("Enter expense amount: ").strip()
    category = input("Enter expense category: ").strip()

    try:
        expense = add_expense(title, amount, category)
        print("Expense added successfully.")
    except ValidationError as e:
        print(f"Error adding expense: {e}")


def handle_view_expenses():
    """Handle viewing all expenses."""
    print("\n--- All Expenses ---")
    expenses = get_all_expenses()
    display_expenses(expenses)
    if expenses:
        print(f"Total: ${get_total():.2f}")


def handle_filter_by_category():
    """Handle filtering expenses by category."""
    print("\n--- Filter Expenses by Category ---")
    category = input("Enter category to filter by: ").strip()
    try:
        filtered_expenses = filter_by_category(category)

        if filtered_expenses:
            print(f"\nExpenses in '{category}':")
            display_expenses(filtered_expenses)
        else:
            print(f"No expenses found in category '{category}'.")

    except ValidationError as e:
        print(f"Error filtering expenses: {e}")


def handle_delete_expense():
    """Handle deleting an expense."""
    print("\n--- Delete Expense ---")
    expenses = get_all_expenses()

    if not expenses:
        print("No expenses to delete.")

    display_expenses(expenses)

    try:
        index = int(input("Enter the index of the expense to delete: ").strip())
        deleted_expense = delete_expense(index)
        print(
            f"\nDeleted: {deleted_expense['title']} - ${deleted_expense['amount']:.2f}"
        )
    except ValueError:
        print("\nError: Please enter a valid number.")
    except ValidationError as e:
        print(f"\nError deleting expense: {e}")


def handle_view_total():
    """Handle viewing total expenses."""
    print("\n--- Total Expenses ---")
    total = get_total()
    print(f"Total Expenses: ${total:.2f}")


# ──────────────────────────────────────────
# Main Application Loop
# ──────────────────────────────────────────


def main():
    """
    Main application loop.
    Displays menu and handles user input until user exits.
    """
    print("Welcome to Expense Tracker!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            handle_add_expense()
        elif choice == "2":
            handle_view_expenses()
        elif choice == "3":
            handle_filter_by_category()
        elif choice == "4":
            handle_view_total()
        elif choice == "5":
            handle_delete_expense()
        elif choice == "6":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# ──────────────────────────────────────────
# Entry Point
# ──────────────────────────────────────────

# This block only runs when file is executed directly
# Not when imported by another file or by behave
if __name__ == "__main__":
    main()
