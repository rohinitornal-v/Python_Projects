"""
test_integration.py - Integration Tests
Tests multiple components working together.
QA/SDET hat - verifies the system as a whole.
Run with: pytest tests/test_integration.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.validator import ValidationError
from app.expense_manager import (
    add_expense,
    get_all_expenses,
    get_total,
    filter_by_category,
    delete_expense,
    load_expenses,
    save_expenses,
)

from tests.test_data.datasets import (
    SINGLE_EXPENSE,
    STANDARD_EXPENSES,
    BEVERAGES_ONLY,
    DELETE_TEST_EXPENSES,
    TOTAL_TEST_EXPENSES,
    TOTAL_TEST_EXPECTED,
    MIXED_CATEGORIES,
)

# -----------------------------------------------------
# Smoke Test - Run these  first after any deployment
# If Fails stop and investigate
# -----------------------------------------------------


class TestSmoke:
    """
    Smoke tests  - quick sanity check
    Use SINGLE_EXPENSE dataset for minimal setup
    """

    def test_can_add_expense(self):
        """Smoke test: Basic add operation works."""
        expense = SINGLE_EXPENSE[0]
        result = add_expense(
            expense["title"],
            expense["amount"],
            expense["category"],
        )
        assert result is not None
        assert result["title"] == expense["title"]

    def test_can_view_expenses(self):
        """Smoke: Basic view operation works."""
        result = get_all_expenses()
        assert isinstance(result, list)

    def test_can_get_total(self):
        """Smoke: Basic total operation works."""
        result = get_total()
        assert isinstance(result, (int, float))

    def test_empty_store_does_not_crash(self):
        """Smoke: Application handles empty store gracefully."""
        assert get_all_expenses() == []
        assert get_total() == 0.00

    def test_add_then_view_works(self):
        """Smoke: Add then view works end to end."""
        save_expenses(SINGLE_EXPENSE)
        expenses = get_all_expenses()
        assert len(expenses) == 1
        assert expenses[0]["title"] == SINGLE_EXPENSE[0]["title"]

    def test_add_then_delete_works(self):
        """SMOKE: Add then delete works end to end."""
        save_expenses(SINGLE_EXPENSE)
        deleted = delete_expense(1)
        assert deleted["title"] == SINGLE_EXPENSE[0]["title"]
        assert get_all_expenses() == []


# ──────────────────────────────────────────
# Integration Tests - Add + View
# ──────────────────────────────────────────


class TestAndView:
    """Tests that add and view work correctly together."""

    def test_standard_expenses_all_appear_in_view(self):
        """All STANDARD_EXPENSES should appear in view"""
        save_expenses(STANDARD_EXPENSES)
        result = get_all_expenses()
        assert len(result) == len(STANDARD_EXPENSES)

    def test_view_always_sorted_descensing(self):
        """View should always show highest amount first."""
        save_expenses(STANDARD_EXPENSES)
        result = get_all_expenses()
        amounts = [e["amount"] for e in result]
        assert amounts == sorted(amounts, reverse=True)

    def test_view_first_item_is_rent(self):
        """FIrst item should be Rent  - highest in STANDARD_EXPENSES."""
        save_expenses(STANDARD_EXPENSES)
        result = get_all_expenses()
        assert result[0]["title"] == "Rent"
        assert result[0]["amount"] == 2000.00

    def test_view_last_item_is_tea(self):
        """Last item should be Tea - lowest in STANDARD_EXPENSES."""
        save_expenses(STANDARD_EXPENSES)
        result = get_all_expenses()
        assert result[-1]["title"] == "Tea"
        assert result[-1]["amount"] == 1.50

    def test_mixed_categories_all_visible(self):
        """All mixed category expenses should appear in view"""
        save_expenses(STANDARD_EXPENSES)
        result = get_all_expenses()
        assert len(result) == len(MIXED_CATEGORIES)


# ---------------------------------------------------
# Integration Tests - Add + Filter
# ---------------------------------------------------


class TestAddAndFilter:
    """Tests that add and filter work correctly together."""

    def test_filter_beverages_from_standard(self):
        """STANDARD_EXPENSES has 2 Beverages — filter should return 2."""
        save_expenses(STANDARD_EXPENSES)
        result = filter_by_category("Beverages")
        assert len(result) == 2
        for e in result:
            assert e["category"] == "Beverages"

    def test_filter_using_beverages_only_dataset(self):
        """BEVERAGES_ONLY dataset — all results should be Beverages."""
        save_expenses(BEVERAGES_ONLY)
        result = filter_by_category("Beverages")
        assert len(result) == len(BEVERAGES_ONLY)

    def test_filter_case_insensitive_from_standard(self):
        """Case insensitive filter should return same count."""
        save_expenses(STANDARD_EXPENSES)
        lower = filter_by_category("beverages")
        upper = filter_by_category("BEVERAGES")
        mixed = filter_by_category("Beverages")
        assert len(lower) == len(upper) == len(mixed) == 2

    def test_filter_sorted_after_add(self):
        """Filtered results should be sorted by amount descending."""
        save_expenses(STANDARD_EXPENSES)
        result = filter_by_category("Beverages")
        amounts = [e["amount"] for e in result]
        assert amounts == sorted(amounts, reverse=True)

    def test_filter_no_match_from_standard(self):
        """Category not in STANDARD_EXPENSES should return empty."""
        save_expenses(STANDARD_EXPENSES)
        result = filter_by_category("Entertainment")
        assert result == []

    def test_filter_all_categories_in_mixed(self):
        """Each category in MIXED_CATEGORIES should be filterable."""
        save_expenses(MIXED_CATEGORIES)
        food = filter_by_category("Food")
        beverages = filter_by_category("Beverages")
        assert len(food) == 2
        assert len(beverages) == 2


# ---------------------------------------------------
# Integration Tests - Add + Delete
# ---------------------------------------------------


class TestAddAndDelete:
    """Tests that add and delete work correctly together."""

    def test_delete_index_1_removes_rent(self):
        """DELETE_TEST_EXPENSES sorted: Rent(1), Lunch(2), Coffee(3).
        Index 1 should remove Rent."""
        save_expenses(DELETE_TEST_EXPENSES)
        delete_expense(1)
        expenses = get_all_expenses()
        title = [e["title"] for e in expenses]
        assert "Rent" not in title
        assert "Coffee" in title
        assert "Lunch" in title

    def test_delete_reduces_count_by_one(self):
        """Count should decrease by 1 after delete."""
        save_expenses(DELETE_TEST_EXPENSES)
        count_before = len(get_all_expenses())
        delete_expense(1)
        count_after = len(get_all_expenses())
        assert count_after == count_before - 1

    def test_delete_all_from_standard(self):
        """Deleting all from STANDARD_EXPENSES should result in empty list."""
        save_expenses(STANDARD_EXPENSES)
        count = len(get_all_expenses())
        for _ in range(count):
            delete_expense(1)
        assert get_all_expenses() == []

    def test_delete_then_add_new_expense(self):
        """Should be able to add after deleting all."""
        save_expenses(DELETE_TEST_EXPENSES)
        count = len(DELETE_TEST_EXPENSES)
        for _ in range(count):
            delete_expense(1)
        expense = SINGLE_EXPENSE[0]
        add_expense(expense["title"], expense["amount"], expense["category"])
        expenses = get_all_expenses()
        assert len(expenses) == 1
        assert expenses[0]["title"] == expense["title"]


# ------------------------------------------
# Integration Tests - Add + Total
# ------------------------------------------


class TestAddAndTotal:
    """Tests that add and total work correctly together."""

    def test_total_matches_standard_expenses_sum(self):
        """Total should match calculated sum of STANDARD_EXPENSES."""
        save_expenses(STANDARD_EXPENSES)
        expected = round(sum(e["amount"] for e in STANDARD_EXPENSES), 2)
        assert get_total() == expected

    def test_total_matches_known_expected(self):
        """Total should match TOTAL_TEST_EXPECTED from datasets.py"""
        save_expenses(TOTAL_TEST_EXPENSES)
        assert get_total() == TOTAL_TEST_EXPECTED

    def test_total_decreases_after_delete(self):
        """Total should be decreased by deleted expense amount."""
        save_expenses(DELETE_TEST_EXPENSES)
        total_before = get_total()
        deleted = delete_expense(1)
        total_after = get_total()
        assert total_after == round(total_before - deleted["amount"], 2)

    def test_total_zero_after_all_deleted(self):
        """Total should be 0.00 after deleting all DELETE_TEST_EXPENSES."""
        save_expenses(DELETE_TEST_EXPENSES)
        count = len(DELETE_TEST_EXPENSES)
        for _ in range(count):
            delete_expense(1)
        assert get_total() == 0.00

    def test_total_single_expense_equals_amount(self):
        """Total of SINGLE_EXPENSE should equal its amount."""
        save_expenses(SINGLE_EXPENSE)
        assert get_total() == SINGLE_EXPENSE[0]["amount"]


# --------------------------------------------------
# Integraton Test - Data Persistence
# ---------------------------------------------------


class TestDataPersistence:
    """Tests that data persists correctly to test file."""

    def test_standard_expenses_persist_to_file(self):
        """STANDARD_EXPENSES should all persist to test data file."""
        save_expenses(STANDARD_EXPENSES)
        loaded = load_expenses()
        assert len(loaded) == len(STANDARD_EXPENSES)

    def test_delete_persists_correctly(self):
        """After deleting Rent, file should not contain Rent."""
        save_expenses(DELETE_TEST_EXPENSES)
        delete_expense(1)
        loaded = load_expenses()
        titles = [e["title"] for e in loaded]
        assert "Rent" not in titles

    def test_multiple_operations_persist(self):
        """Add, delete, add operations should all persist correctly."""
        save_expenses(DELETE_TEST_EXPENSES)
        delete_expense(1)  # delete Rent
        expense = SINGLE_EXPENSE[0]
        add_expense(expense["title"], expense["amount"], expense["category"])
        loaded = load_expenses()
        titles = [e["title"] for e in loaded]
        assert "Rent" not in titles
        assert expense["title"] in titles

    def test_production_data_not_affected(self):
        """Test data should use test data file not production file."""
        production_file = os.path.abspath("data/expenses.json")
        test_file = os.environ.get("EXPENSE_DATA_FILE", "")
        assert (
            os.path.abspath(test_file) != production_file
        ), "Tests are using production data file!"


# --------------------------------------------------
# Integration Tests - Logging
# --------------------------------------------------


class TestLogging:
    """Tests that logging works correctly with operations."""

    def test_add_creates_info_log(self):
        """Adding expenses should write INFO entry to test log."""
        log_file = os.environ.get("EXPENSE_LOG_FILE", "logs/app.log")
        expense = SINGLE_EXPENSE[0]
        add_expense(expense["title"], expense["amount"], expense["category"])
        with open(log_file, "r") as f:
            contents = f.read()
        assert "INFO" in contents
        assert expense["title"] in contents

    def test_invalid_delete_creates_warning_log(self):
        """Invaclid entry should write WARNING entry to test log."""
        log_file = os.environ.get("EXPENSE_LOG_FILE", "logs/app.log")
        save_expenses(SINGLE_EXPENSE)
        try:
            delete_expense(99)
        except ValidationError:
            pass
        with open(log_file, "r") as f:
            contents = f.read()
        assert "WARNING" in contents

    def test_valid_delete_creates_info_log(self):
        """Valid delete should write INFO entry to test log."""
        log_file = os.environ.get("EXPENSE_LOG_FILE", "logs/app.log")
        save_expenses(DELETE_TEST_EXPENSES)
        delete_expense(1)
        with open(log_file, "r") as f:
            contents = f.read()
        assert "INFO" in contents

    def test_test_log_not_production_log(self):
        """Tests should write to test log not production log."""
        production_log = os.path.abspath("logs/app.log")
        test_log = os.path.abspath(os.environ.get("EXPENSE_LOG_FILE", "logs/app.log"))
        assert test_log != production_log, "Tests are writing to production log file!"
