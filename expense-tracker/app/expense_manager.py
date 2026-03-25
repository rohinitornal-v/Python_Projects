"""expense_manager.py - Core Business Logic
Handles all expense operations for the Expense Tracker.
This is the heart of the application.
"""

import json
import os

from app.logger import log_info, log_warning

from app.validator import (
    validate_title,
    validate_amount,
    validate_category,
    validate_index,
    ValidationError,
)

# Path to expenses data file
DATA_FILE = "data/expenses.json"

# -------------------------------------
# File Operation
# --------------------------------------


def load_expenses():
    """Load all expenses from the JSON file."""

    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, ValueError):
        print("Warning: expense.json file is corrupted : Starting fresh.")
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


# -------------------------------------
# Expense Manager - Core Operations
# --------------------------------------


def add_expense(title, amount, category):
    """Add a new expense after validating the input."""
    validate_title(title)
    amount = validate_amount(amount)
    validate_category(category)

    new_expense = {
        "title": title.strip(),
        "amount": amount,
        "category": category.strip(),
    }

    expenses = load_expenses()
    expenses.append(new_expense)
    save_expenses(expenses)

    # Log the successful operation at INFO level

    log_info(f"Added expense: {title} - ${amount:.2f} in category '{category}'")
    return new_expense


def get_all_expenses():
    """Get all expenses
    - Returns sorted by amount descending
    - Highest amount appears first.
    - Returns empty list if no expenses
    """
    expenses = load_expenses()

    return sorted(expenses, key=lambda x: x["amount"], reverse=True)


def filter_by_category(category):
    """
    Filter expenses by category
    - Case insensitive match
    - Returns sorted by amount descending
    - Returns empty list if no matches
    """

    validate_category(category)
    expenses = load_expenses()
    filtered = [
        expense
        for expense in expenses
        if expense["category"].lower() == category.lower()
    ]

    return sorted(filtered, key=lambda x: x["amount"], reverse=True)


def delete_expense(index):
    """
    Delete expense by index
    - Index is 1-based
    - Index refers to position in sorted list
    - Validates index range
    - Returns deleted expense
    """
    expenses = load_expenses()
    try:
        validate_index(index, expenses)
    except ValidationError:
        log_warning(f"Invalid delete index: {index}")
        raise
    # Sort to match what user sees on screen
    sorted_expenses = sorted(expenses, key=lambda x: x["amount"], reverse=True)

    # Get expense to delete from sorted list
    expense_to_delete = sorted_expenses[index - 1]

    # Remove from original unsorted list
    expenses.remove(expense_to_delete)

    # Save updated list back to the file
    save_expenses(expenses)
    log_info(
        f"Deleted expense: {expense_to_delete['title']} - ${expense_to_delete['amount']:.2f}"
    )
    return expense_to_delete


def get_total():
    """
    Calculate total spending
    - Returns sum of all expense amounts
    - Returns 0.00 if no expenses exist
    """
    expenses = load_expenses()
    return round(sum(e["amount"] for e in expenses), 2)
