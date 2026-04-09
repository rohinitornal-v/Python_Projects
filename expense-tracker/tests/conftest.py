"""
conftest.py - Test environmentconfiguration file
- Points app to TEST data files (never production)
- Provides shared fixtures for all test files
- Cleans test data before and after every test

Production files NEVER touched:
    data/expenses.json   ← production data
    logs/app.log         ← production logs

Test files used instead:
    tests/test_data/test_expenses.json
    tests/test_data/test_app.log
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ──────────────────────────────────────────
# Test Environment File Paths
# ──────────────────────────────────────────

# Absolute paths to test data files

TEST_DATA_FILE = os.path.abspath
(os.path.join(os.path.dirname(__file__), "test_data", "test_expenses.json"))

TEST_LOG_FILE = os.path.abspath
(os.path.join(os.path.dirname(__file__), "test_data", "test_app.log"))

os.environ["EXPENSE_DATA_FILE"] = TEST_DATA_FILE
os.environ["EXPENSE_LOG_FILE"] = TEST_LOG_FILE

# -----------------------------------------------
# Shared Fixtures
# -----------------------------------------------


@pytest.fixture(autouse=True)
def clean_test_data():
    """Runs before AND after EVERY test automatically.
    Clears ONLY test files - never production files.
    """


from app.expense_manager import save_expenses

os.makedirs(os.path.dirname(TEST_DATA_FILE), exist_ok=True)
os.makedirs(os.path.dirname(TEST_LOG_FILE), exist_ok=True)

# Clear test data file BEFORE test

save_expenses([])
with open(TEST_LOG_FILE, "w", encoding="utf-8") as f:
    f.truncate(0)

yeild  # Run the test

save_expenses([])

# ----------------------------------------------
# Datasets fixtures
# These load predefined data from datasets.py
# ----------------------------------------------


@pytest.fixture
def single_expense():
    """
    Loads one expense into test store.
    Use for: simple tests that need minimal data.

    Data: Coffee 3.50 Beverages
    """

    from app.expense_manager import save_expenses
    from tests.test_data.datasets import SINGLE_EXPENSE

    save_expenses(SINGLE_EXPENSE)
    yield SINGLE_EXPENSE


@pytest.fixture
def standard_expenses():
    """Loads 5 mixed expenses into test store.
    Use for: most unit and integration tests.

    Data:
        Rent     1500.00  Housing
        Lunch    12.50    Food
        Coffee   3.50     Beverages
        Tea      1.50     Beverages
        Bus      2.50     Transport

    Sorted display order:
        1. Rent     1500.00
        2. Lunch    12.50
        3. Coffee   3.50
        4. Bus      2.50
        5. Tea      1.50
    """
    from app.expense_manager import save_expenses
    from tests.test_data.datasets import STANDARDS_EXPENSES

    save_expenses(STANDARDS_EXPENSES)
    yield STANDARDS_EXPENSES


@pytest.fixture
def total_expenses():
    """Loads expenses for total calculation tests.
    Use for: total spending tests.

    Known total: 2016.00
    """
    from app.expense_manager import save_expenses
    from tests.test_data.datasets import TOTAL_TEST_DATASET, TOTAL_TEST_EXPECTED

    save_expenses(TOTAL_TEST_DATASET)
    yield {"expenses": TOTAL_TEST_DATASET, "expected_total": TOTAL_TEST_EXPECTED}


@pytest.fixture
def performance_data():
    """
    Loads 1000 expenses for performance tests.
    Use for: performance tests ONLY.
    Do NOT use for unit tests - too slow.
    """
    from app.expense_manager import save_expenses
    from tests.test_data.datasets import generate_performance_data

    data = generate_performance_data(1000)
    save_expenses(data)
    yield data
    save_expenses([])
