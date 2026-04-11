"""
datasets.py - Shared Test Datasets
Single source of truth for all test data.
Used by pytest tests, behave steps and fixtures.

Never modify this file during tests - read only.
"""

# ──────────────────────────────────────────
# Single Expense Dataset
# Use for: simple unit tests
# ──────────────────────────────────────────

SINGLE_EXPENSE = [{"title": "Coffee", "amount": 3.50, "category": "Beverages"}]

# ──────────────────────────────────────────
# Standard Dataset
# Use for: most unit and integration tests
# Contains mix of categories and amounts
# ──────────────────────────────────────────

STANDARD_EXPENSES = [
    {"title": "Rent", "amount": 2000.00, "category": "Housing"},
    {"title": "Lunch", "amount": 12.50, "category": "Food"},
    {"title": "Coffee", "amount": 3.50, "category": "Beverages"},
    {"title": "Tea", "amount": 1.50, "category": "Beverages"},
    {"title": "Bus", "amount": 2.50, "category": "Transport"},
]

# ──────────────────────────────────────────
# Category Specific Datasets
# Use for: filter tests
# ──────────────────────────────────────────

BEVERAGES_ONLY = [
    {"title": "Coffee", "amount": 3.50, "category": "Beverages"},
    {"title": "Tea", "amount": 1.50, "category": "Beverages"},
    {"title": "Soda", "amount": 3.00, "category": "Beverages"},
]

FOOD_ONLY = [
    {"title": "Lunch", "amount": 12.50, "category": "Food"},
    {"title": "Dinner", "amount": 25.50, "category": "Food"},
    {"title": "BreakFast", "amount": 10.50, "category": "Food"},
]

MIXED_CATEGORIES = [
    {"title": "Movie", "amount": 150.00, "category": "Entertainment"},
    {"title": "Gym", "amount": 120.00, "category": "Fitness"},
    {"title": "Coffee", "amount": 3.50, "category": "Beverages"},
    {"title": "Tea", "amount": 1.50, "category": "Beverages"},
    {"title": "Pizza", "amount": 15.00, "category": "Food"},
    {"title": "Bus", "amount": 2.50, "category": "Transport"},
    {"title": "Rent", "amount": 2000.00, "category": "Housing"},
]


# ──────────────────────────────────────────
# Delete Test Dataset
# Use for: delete tests
# Known sorted order: Rent(1), Lunch(2), Coffee(3)
# ──────────────────────────────────────────

DELETE_TEST_EXPENSES = [
    {"title": "Coffee", "amount": 3.50, "category": "Beverages"},
    {"title": "Lunch", "amount": 12.50, "category": "Food"},
    {"title": "Rent", "amount": 2000.00, "category": "Housing"},
]

# Sorted display order:
# index 1 → Rent    2000.00
# index 2 → Lunch   12.50
# index 3 → Coffee  3.50

# ──────────────────────────────────────────
# Total Test Dataset
# Use for: total calculation tests
# Known total: 2016.00
# ──────────────────────────────────────────

TOTAL_TEST_EXPENSES = [
    {"title": "Coffee", "amount": 3.50, "category": "Beverages"},
    {"title": "Lunch", "amount": 12.50, "category": "Food"},
    {"title": "Rent", "amount": 2000.00, "category": "Housing"},
]

TOTAL_TEST_EXPECTED = 2016.00

# ──────────────────────────────────────────
# Performance Dataset
# Use for: performance tests ONLY
# 1000 expenses - do not use for unit tests
# ──────────────────────────────────────────


def generate_performance_data(count=1000):
    """
    Generate large dataset for performance testing.
    Called as function to avoid loading 1000 records in memory
    unless explicitly needed.
    """
    return [
        {
            "title": f"Expense {i + 1}",
            "amount": float(i + 1),
            "category": "Food" if i % 2 == 0 else "Transport",
        }
        for i in range(count)
    ]
