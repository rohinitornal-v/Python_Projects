"""
test_expense_manager.py - pytest Unit Tests
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.validator import ValidationError
from app.expense_manager import (
    add_expense,
    get_all_expenses,
    filter_by_category,
    delete_expense,
    get_total,
    save_expenses,
    load_expenses,
)

# --------------------
# Fixtures
# --------------------


@pytest.fixture(autouse=True)
def clean_expenses():
    """
    Runs before AND after every test automatically.
    autouse=True means no need to call it explicitly.
    Ensures every test starts with empty expense store.
    """
    save_expenses([])  # clean before test
    yield  # test runs here
    save_expenses([])  # clean after test


# -------------------------
# Tests -add expense
# -------------------------


class TestExpense:
    """Test for add_expense function."""

    def test_add_valid_expense(self):
        """Valid Expense should be added and returned."""
        result = add_expense("Coffee", 3.50, "Beverages")
        assert result["title"] == "Coffee"
        assert result["amount"] == 3.50
        assert result["category"] == "Beverages"

    def test_add_expense_persists(self):
        """Added expense should be saved to expenses.json"""
        add_expense("Coffee", 3.50, "Beverages")
        expenses = load_expenses()
        assert len(expenses) == 1
        assert expenses[0]["title"] == "Coffee"

    def test_add_multiple_expenses(self):
        """Multiple expenses should all be saved."""
        add_expense("Coffee", 3.50, "Beverages")
        add_expense("Lunch", 12.50, "Food")
        add_expense("Rent", 1500.00, "Housing")
        expenses = load_expenses()
        assert len(expenses) == 3

    def test_add_expense_returns_dict(self):
        """add_expense should return a dictionary."""
        result = add_expense("Coffee", 3.50, "Beverages")
        assert isinstance(result, dict)

    def test_add_expense_amount_stored_as_float(self):
        "Amount should be stored as float."
        result = add_expense("Coffee", 3, "Beverages")
        assert isinstance(result["amount"], float)

    def test_add_empty_title_raises_error(self):
        "Empty tile should raise ValidationError"
        with pytest.raises(ValidationError):
            add_expense("", 10.00, "Misc")

    def test_add_zero_amount_raises_error(self):
        "Zero amount should raise validationError."
        with pytest.raises(ValidationError):
            add_expense("Tea", 0, "Beverages")

    def test_add_negative_amount_raises_error(self):
        "Negative amount should raise ValidationError."
        with pytest.raises(ValidationError):
            add_expense("Tea", -3, "Beverages")

    def test_add_non_numeric_amount_raises_error(self):
        "Non-numeric amount should raise ValidationError."
        with pytest.raises(ValidationError):
            add_expense("Tea", "jkl", "Beverages")

    def test_add_invalid_expense_not_saved(self):
        "Invalid expense should not be saved to file."
        try:
            add_expense("", 3.50, "Beverages")
        except ValidationError:
            pass
        expenses = load_expenses()
        assert len(expenses) == 0


# ---------------------------
# Test - get_all_expenses
# ---------------------------


class TestGetAllExpenses:
    """Tests for get_all_expenses function."""

    def test_returns_empty_list(self):
        """Should return empty list when no expenses exist."""
        result = get_all_expenses()
        assert result == []

    def test_returns_all_expenses(self):
        """Should return all stored expenses."""
        add_expense("Rent", 1500.00, "Housing")
        add_expense("Movie", 15.00, "Entertainment")
        result = get_all_expenses()
        assert len(result) == 2

    def test_sorted_by_amount_descending(self):
        """Expenses should be sorted by amount descending."""
        add_expense("Veggies", 15.00, "Grocceries")
        add_expense("Chips", 3.00, "Snacks")
        add_expense("Lunch", 12.50, "Food")
        result = get_all_expenses()
        assert result[0]["title"] == "Veggies"
        assert result[1]["title"] == "Lunch"
        assert result[2]["title"] == "Chips"

    def test_highest_amount_first(self):
        """Highest amount should appear first."""
        add_expense("Coffee", 3.50, "Beverages")
        add_expense("Rent", 1500.00, "Housing")
        result = get_all_expenses()
        assert result[0]["amount"] == 1500.00

    def test_lowest_amount_last(self):
        """Lowest amount should appear last."""
        add_expense("Coffee", 3.50, "Beverages")
        add_expense("Rent", 1500.00, "Housing")
        add_expense("Tea", 1.50, "Beverages")
        result = get_all_expenses()
        assert result[-1]["amount"] == 1.50

    def test_returns_list(self):
        """get_all_expenses should always return a list."""
        result = get_all_expenses()
        assert isinstance(result, list)


# ------------------------------
# Tests - filter by category
# ------------------------------


class TestFilterByCategory:
    """Tests for filter_by_category function."""

    def setup_method(self):
        """Add test expenses before each test"""
        save_expenses([])
        add_expense("Stiching material", 12.00, "Arts n Crafts")
        add_expense("Necklace", 150.00, "Jewelery")
        add_expense("Books", 50.00, "Liesure")
        add_expense("Coffee", 3.50, "Beverages")
        add_expense("Tea", 1.50, "Beverages")
        add_expense("Lunch", 12.50, "Food")
        add_expense("Rent", 1500.00, "Housing")

    def test_filter_exact_match(self):
        """Should return only expenses matching category."""
        result = filter_by_category("Beverages")
        assert len(result) == 2
        for e in result:
            assert e["category"] == "Beverages"

    def test_filter_case_insensitive_lower(self):
        """Lowercase category should match."""
        result = filter_by_category("beverages")
        assert len(result) == 2

    def test_filter_case_insensitive_upper(self):
        """Uppercase category should match."""
        result = filter_by_category("BEVERAGES")
        assert len(result) == 2

    def test_filter_no_match_returns_empty(self):
        """No matching category should return empty list."""
        result = filter_by_category("Entertainment")
        assert result == []

    def test_filter_results_sorted_descending(self):
        """Filtered results should be sorted by amount descending."""
        result = filter_by_category("Beverages")
        amounts = [e["amount"] for e in result]
        assert amounts == sorted(amounts, reverse=True)

    def test_filter_empty_category_raises_error(self):
        """Empty category should raise ValidationError."""
        with pytest.raises(ValidationError):
            filter_by_category("")

    def test_filter_returns_list(self):
        """filter_by_category should always return a list."""
        result = filter_by_category("Food")
        assert isinstance(result, list)


# -------------------------
# Test - delete_expense
# -------------------------


class TestDeleteExpense:
    """Test for delete_expense function."""

    def setup_method(self):
        """Add test expenses before each test."""
        save_expenses([])
        add_expense("Coffee", 3.50, "Beverages")
        add_expense("Rent", 1500.00, "Housing")

    def test_delete_valid_expense(self):
        """Valid index should delete and return expense."""
        result = delete_expense(2)
        assert result["title"] == "Rent"

    def test_delete_reduces_count(self):
        """Deleting expense should reduce count by 1."""
        delete_expense(1)
        expenses = load_expenses()
        assert len(expenses) == 1

    def test_deleted_expense_not_in_list(self):
        """Deleted expense should not appear in list."""
        deleted = delete_expense(1)
        expenses = load_expenses()
        titles = [e["title"] for e in expenses]
        assert deleted["title"] not in titles

    def test_delete_persists_to_file(self):
        """Deleted expense should be saved to espense.json"""
        deleted = delete_expense(1)
        loaded = load_expenses()
        titles = [e["title"] for e in loaded]
        assert deleted["title"] not in titles

    def test_delete_returns_deleted_expense(self):
        """delete_expense should return the deleted expense."""
        result = delete_expense(1)
        assert isinstance(result, dict)
        assert "title" in result
        assert "amount" in result
        assert "category" in result

    def test_delete_zero_index_raises_error(self):
        """Zero index should raise ValidationError."""
        with pytest.raises(ValidationError):
            delete_expense(0)

    def test_delete_negative_index_raises_error(self):
        """Negative index should raise ValidationError."""
        with pytest.raises(ValidationError):
            delete_expense(-1)

    def test_delete_out_of_range_raises_error(self):
        """Out of range index should raise ValidationError."""
        with pytest.raises(ValidationError):
            delete_expense(99)

    def test_delete_empty_store_raises_error(self):
        """Deleting from empty store should raise ValidationError."""
        save_expenses([])
        with pytest.raises(ValidationError) as exc_info:
            delete_expense(1)
        assert "No expenses found" in str(exc_info.value)


# ──────────────────────────────────────────
# Tests - get_total
# ──────────────────────────────────────────


class TestGetTotal:
    """Tests for get_total function."""

    def test_total_no_expenses(self):
        """Total should be 0.00 when no expenses exist."""
        result = get_total()
        assert result == 0.00

    def test_total_single_expense(self):
        """Total should equal single expense amount."""
        add_expense("Coffee", 3.50, "Beverages")
        result = get_total()
        assert result == 3.50

    def test_total_multiple_expenses(self):
        """Total should be sum of all expense amounts."""
        add_expense("Coffee", 3.50, "Beverages")
        add_expense("Lunch", 12.50, "Food")
        add_expense("Rent", 1500.00, "Housing")
        result = get_total()
        assert result == 1516.00

    def test_total_is_numeric(self):
        """Total should always return numeric value."""
        result = get_total()
        assert isinstance(result, (int, float))

    def test_total_rounded_two_decimals(self):
        """Total should be rounded to 2 decimal places."""
        add_expense("Coffee", 3.33, "Beverages")
        add_expense("Tea", 1.11, "Beverages")
        result = get_total()
        assert result == round(result, 2)

    def test_total_after_delete(self):
        """Total should update correctly after deletion."""
        add_expense("Coffee", 3.50, "Beverages")
        add_expense("Lunch", 12.50, "Food")
        delete_expense(2)  # deletes Lunch (highest)
        result = get_total()
        assert result == 3.50
