"""expense_manager.py - Core Business Logic
Handles all expense operations for the Expense Tracker.
This is the heart of the application.
"""

import json
import os

from app.logger import logger, setup_logger

logger = setup_logger()

from app.validator import (
    validate_title,
    validate_amount,
    validate_category,
    validate_index,
    ValidationError,
)

# Path to expenses data file
DATA_FILE = os.environ.get("EXPENSE_DATA_FILE", "data/expenses.json")


# -------------------------------------
# File Operations
# -------------------------------------


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
# -------------------------------------


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

    logger.info(f"Added expense: {title}, Amount: {amount}, Category: {category}")
    return new_expense


def get_all_expenses():
    """Get all expenses sorted by amount descending."""
    expenses = load_expenses()
    return sorted(expenses, key=lambda x: x["amount"], reverse=True)


def filter_by_category(category):
    """Filter expenses by category (case-insensitive) sorted by amount descending."""
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
    Delete expense by index (1-based)
    - Raises ValidationError for invalid index
    - Returns deleted expense
    """
    from app.logger import log_info, log_warning, ensure_log_file

    ensure_log_file()

    expenses = load_expenses()

    if not expenses:
        log_warning("No expenses found")
        raise ValidationError("No expenses found")

    if index <= 0 or index > len(expenses):
        log_warning(f"Invalid delete index: {index}")
        raise ValidationError("Invalid Index")

    # Delete using original order
    deleted = expenses.pop(index - 1)

    save_expenses(expenses)

    log_info(f"Deleted expense at index: {index}")

    return deleted


def get_total():
    """Calculate total spending (sum of amounts)."""
    expenses = load_expenses()
    return round(sum(e["amount"] for e in expenses), 2)
