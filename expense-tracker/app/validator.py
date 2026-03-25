"""Validator Functions for Expense Tracker"""


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


# ──────────────────────────────────────────
# Validation Functions
# ──────────────────────────────────────────


def validate_title(title):
    """Validate expense title
    - Must not be empty
    """
    if not title or title.strip() == "":
        raise ValidationError("Title cannot be empty.")


def validate_amount(amount):
    """Validate expense amount
    - Must be numeric
    - Must be greater than 0
    """
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValidationError("Amount must be a number.")
    if amount <= 0:
        raise ValidationError("Amount must be greater than 0.")
    return amount


def validate_category(category):
    """Validate expense category
    - Must not be empty
    """
    if not category or category.strip() == "":
        raise ValidationError("Category cannot be empty.")


def validate_index(index, expenses):
    """Validate index for editing/deleting expenses
    - Must be greater than 0
    - Must be within the valid range
    """
    if not expenses:
        raise ValidationError("No expenses found.")
    # Check index is within valid range
    if index <= 0 or index > len(expenses):
        raise ValidationError("Index must be greater than 0.")
