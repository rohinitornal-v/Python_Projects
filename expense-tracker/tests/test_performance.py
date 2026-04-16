"""
test_performance.py - Performance Tests
Tests application handles large datasets within acceptable time.

All test data comes from tests/test_data/datasets.py
Uses generate_performance_data(1000) for 1000 expense dataset.

Run separately from other tests:
    pytest tests/test_performance.py -v

Run before major releases only — slow tests.
"""

import time
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.expense_manager import (
    get_all_expenses,
    filter_by_category,
    delete_expense,
    get_total,
    save_expenses,
)
from tests.test_data.datasets import generate_performance_data

# Acceptable response time threshold
THRESHOLD = 2.0  # seconds
DATASET_SIZE = 1000


class TestPerformance:
    """
    Performance tests with 1000 expenses from datasets.py.
    generate_performance_data(1000) creates:
        500 Food expenses   (even index)
        500 Transport       (odd index)
        Amounts: 1.0 to 1000.0
    """

    def setup_method(self):
        """
        Generate and save 1000 expenses once before each test.
        Uses datasets.generate_performance_data() — not hardcoded.
        """
        data = generate_performance_data(DATASET_SIZE)
        save_expenses(data)

    def teardown_method(self):
        """Clean up test data after each performance test."""
        save_expenses([])

    def test_view_all_1000_expenses_under_threshold(self):
        """
        Viewing 1000 expenses should complete under 2 seconds.
        Verifies sort operation scales correctly.
        """
        start = time.time()
        result = get_all_expenses()
        elapsed = time.time() - start

        assert (
            len(result) == DATASET_SIZE
        ), f"Expected {DATASET_SIZE} expenses but got {len(result)}"
        assert (
            elapsed < THRESHOLD
        ), f"View took {elapsed:.3f}s — exceeds {THRESHOLD}s threshold"

        # Log actual time for visibility
        print(f"\n  View time: {elapsed:.3f}s")

    def test_filter_1000_expenses_under_threshold(self):
        """
        Filtering 1000 expenses by category should complete under 2 seconds.
        500 Food expenses in performance dataset.
        """
        start = time.time()
        result = filter_by_category("Food")
        elapsed = time.time() - start

        assert (
            len(result) == DATASET_SIZE // 2
        ), f"Expected {DATASET_SIZE // 2} Food expenses but got {len(result)}"
        assert (
            elapsed < THRESHOLD
        ), f"Filter took {elapsed:.3f}s — exceeds {THRESHOLD}s threshold"

        print(f"\n  Filter time: {elapsed:.3f}s")

    def test_total_1000_expenses_under_threshold(self):
        """
        Calculating total of 1000 expenses should complete under 2 seconds.
        Expected total: sum of 1.0 to 1000.0 = 500500.0
        """
        expected_total = sum(float(i + 1) for i in range(DATASET_SIZE))

        start = time.time()
        result = get_total()
        elapsed = time.time() - start

        assert isinstance(result, (int, float)), "Total should be numeric"
        assert result == round(
            expected_total, 2
        ), f"Expected total {expected_total} but got {result}"
        assert (
            elapsed < THRESHOLD
        ), f"Total took {elapsed:.3f}s — exceeds {THRESHOLD}s threshold"

        print(f"\n  Total time: {elapsed:.3f}s")

    def test_delete_from_1000_expenses_under_threshold(self):
        """
        Deleting from 1000 expenses should complete under 2 seconds.
        Index 1 deletes expense with amount 1000.0 (highest).
        """
        start = time.time()
        result = delete_expense(1)
        elapsed = time.time() - start

        assert result is not None, "Delete should return deleted expense"
        assert result["amount"] == float(
            DATASET_SIZE
        ), f"Expected amount {float(DATASET_SIZE)} but got {result['amount']}"
        assert (
            elapsed < THRESHOLD
        ), f"Delete took {elapsed:.3f}s — exceeds {THRESHOLD}s threshold"

        print(f"\n  Delete time: {elapsed:.3f}s")
