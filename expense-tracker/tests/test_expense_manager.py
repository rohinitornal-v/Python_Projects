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

#--------------------
# Fixtures
#--------------------

@pytest.fixture(autouse=True)

def clean_expenses()
   """
    Runs before AND after every test automatically.
    autouse=True means no need to call it explicitly.
    Ensures every test starts with empty expense store.
  """
  save_expenses([])   # clean before test
  yield               # test runs here
  save_expenses([])   # clean after test
