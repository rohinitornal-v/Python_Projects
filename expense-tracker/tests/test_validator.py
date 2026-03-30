"""
test_validator.py - pytest Unit Tests for validator.py
Run with: pytest tests/test_validator.py -v
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.validator import (
    validate_title,
    validate_amount,
    validate_category,
    validate_index,
    ValidationError,
)

# ──────────────────────────────────────────
# Tests - validate_title
# ──────────────────────────────────────────


class TestValidateTitle:
    """Tests for validate_title function."""

    def test_valid_title_passes(self):
        """Valid title should not raise any error."""
        validate_title("Coffee")  # should not raise

    def test_empty_title_raises_error(self):
        """Empty title should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_title("")
        assert "Title cannot be empty" in str(exc_info.value)

    def test_whitespace_title_raises_error(self):
        """Whitespace only title should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_title("   ")

    def test_none_title_raises_error(self):
        """None title should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_title(None)


# ──────────────────────────────────────────
# Tests - validate_amount
# ──────────────────────────────────────────


class TestValidateAmount:
    """Tests for validate_amount function."""

    def test_valid_amount_passes(self):
        """Valid positive amount should return float."""
        result = validate_amount(10.50)
        assert result == 10.50

    def test_valid_string_amount_passes(self):
        """String number should be converted to float."""
        result = validate_amount("25.00")
        assert result == 25.00

    def test_zero_amount_raises_error(self):
        """Zero amount should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_amount(0)
        assert "Amount must be greater than 0." in str(exc_info.value)

    def test_negative_amount_raises_error(self):
        """Negative amount should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_amount(-5)
        assert "Amount must be greater than 0." in str(exc_info.value)

    def test_non_numeric_amount_raises_error(self):
        """Non-numeric amount should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_amount("abc")
        assert "numeric" in str(exc_info.value)

    def test_amount_returns_float(self):
        """validate_amount should always return float."""
        result = validate_amount(10)
        assert isinstance(result, float)


# ──────────────────────────────────────────
# Tests - validate_category
# ──────────────────────────────────────────


class TestValidateCategory:
    """Tests for validate_category function."""

    def test_valid_category_passes(self):
        """Valid category should not raise error."""
        validate_category("Food")  # should not raise

    def test_empty_category_raises_error(self):
        """Empty category should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_category("")
        assert "Category cannot be empty" in str(exc_info.value)

    def test_whitespace_category_raises_error(self):
        """Whitespace only category should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_category("   ")


# ──────────────────────────────────────────
# Tests - validate_index
# ──────────────────────────────────────────


class TestValidateIndex:
    """Tests for validate_index function."""

    def setup_method(self):
        """Set up test expenses list before each test."""
        self.expenses = [
            {"title": "Coffee", "amount": 3.50, "category": "Beverages"},
            {"title": "Lunch", "amount": 12.50, "category": "Food"},
            {"title": "Rent", "amount": 1500.00, "category": "Housing"},
        ]

    def test_valid_index_passes(self):
        """Valid index should not raise error."""
        validate_index(2, self.expenses)  # should not raise

    def test_first_index_passes(self):
        """Index 1 should be valid."""
        validate_index(1, self.expenses)  # should not raise

    def test_last_index_passes(self):
        """Last index should be valid."""
        validate_index(3, self.expenses)  # should not raise

    def test_zero_index_raises_error(self):
        """Zero index should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_index(0, self.expenses)
        assert "Invalid Index" in str(exc_info.value)

    def test_negative_index_raises_error(self):
        """Negative index should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_index(-1, self.expenses)

    def test_out_of_range_raises_error(self):
        """Out of range index should raise ValidationError."""
        with pytest.raises(ValidationError):
            validate_index(99, self.expenses)

    def test_empty_list_raises_error(self):
        """Empty expense list should raise ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            validate_index(1, [])
        assert "No expenses found" in str(exc_info.value)
