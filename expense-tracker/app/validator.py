"""Validator Functions for Expense Tracker"""


class ValidationError(Exception):
    """Custom exception for validation errors."""

    pass


# def validate_non_empty_string(value, field_name):
#   """
#  Validate that the input is a non-empty string.
# """
# if not isinstance(value, str) or not value.strip():
#   raise ValidationError(f"{field_name} must be a non-empty string.")
# return value.strip()


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
    if index <= 0 or index > len(expenses):
        raise ValidationError("Index must be greater than 0.")
