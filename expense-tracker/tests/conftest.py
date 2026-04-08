"""
conftest.py - pytest configuration file
Adds project root to Python path so imports work correctly
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ──────────────────────────────────────────
# Test Environment Configuration
# ──────────────────────────────────────────
# Use separate files for testing so dev data is never touched

os.environ["EXPENSE_DATA_FILE"] = "data/test_expenses.json"
os.environ["EXPENSE_LOG_FILE"] = "logs/test_app.log"


@pytest.fixture
def sample_expenses():
    return [
        {"title": "Coffee", "amount": 3.50, "category": "Beverages"},
        {"title": "Lunch", "amount": 15.00, "category": "Food"},
        {"title": "Taxi", "amount": 20.00, "category": "Transport"},
        {"title": "Groceries", "amount": 85.40, "category": "Food"},
        {"title": "Internet Bill", "amount": 60.00, "category": "Utilities"},
        {"title": "Electricity Bill", "amount": 120.75, "category": "Utilities"},
        {"title": "Gym Membership", "amount": 49.99, "category": "Fitness"},
        {"title": "Movie Ticket", "amount": 12.00, "category": "Entertainment"},
        {"title": "Dinner", "amount": 35.25, "category": "Food"},
        {"title": "Bus Ticket", "amount": 2.50, "category": "Transport"},
        {"title": "Uber Ride", "amount": 18.75, "category": "Transport"},
        {"title": "Books", "amount": 45.00, "category": "Education"},
        {"title": "Stationery", "amount": 9.99, "category": "Education"},
        {"title": "Rent", "amount": 1500.00, "category": "Housing"},
        {"title": "Tea", "amount": 1.75, "category": "Beverages"},
    ]
