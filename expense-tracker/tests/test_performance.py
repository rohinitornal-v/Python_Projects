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
