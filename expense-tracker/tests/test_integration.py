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
    assert result["title“] == expense["title"]"]

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
        result =get_all_expenses()
        assert len(result) == len(STANDARD_EXPENSES)

    def test_view_always_sorted_descensing(self):
        """View should always show highest amount first."""
        save_expenses(STANDARD_EXPENSES)
        result = get_all_expenses()
        amounts = [e["amount"]for e in result]
        assert amounts == sorted (amounts, reverse=True)

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
        """ All mixed category expenses should appear in view"""
        save_expenses(STANDARD_EXPENSES)
        result = get_all_expenses()
        assert len(result) == len(MIXED_CATEGORIES)


