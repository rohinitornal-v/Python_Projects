"""Quick tests for validator.py"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.validator import (
    validate_title,
    validate_amount,
    validate_category,
    validate_index,
    ValidationError,
)

print("=" * 50)
print("Testing validator.py")
print("=" * 50)

# Test validate_title

print("\n -------- Validate Title --------")
# Test 1 - empty title
try:
    validate_title("")
except ValidationError as e:
    print(f"Test 01 passed: {e}")

# Test 2 - whitespace only title
try:
    validate_title("   ")
except ValidationError as e:
    print(f"Test 02 passed: {e}")

# Test 3 - valid title
try:
    validate_title("Coffee")
    print("Test 03 passed: Valid title accepted")
except ValidationError as e:
    print(f"Test 03 failed: {e}")

# Test validate_amount

print("\n -------- Validate Amount --------")

# Test 4 - Zero amount

try:
    validate_amount(0)
except ValidationError as e:
    print(f"Test 04 passed: {e}")

# Test 5 - Negative amount
try:
    validate_amount(-10)
except ValidationError as e:
    print(f"Test 05 passed: {e}")

# Test 6 - Non-numeric amount
try:
    validate_amount("9abc")
except ValidationError as e:
    print(f"Test 06 passed: {e}")

# Test 7 - Valid amount
try:
    result = validate_amount(25.50)
    print(f"Test 07 passed: Valid amount accepted → {result}")
except ValidationError as e:
    print(f"Test 07 failed: {e}")

# Test 8 - string number is accepted
try:
    result = validate_amount("25.00")
    print(f"Test 08 passed: string number accepted → {result}")
except ValidationError as e:
    print(f"Test 08 FAILED: {e}")

# Test validate_category

print("\n -------- Validate Category --------")

# Test 9 - empty category
try:
    validate_category("")
except ValidationError as e:
    print(f"Test 09 passed: {e}")

# Test 10 - whitespace only category
try:
    validate_category("   ")
except ValidationError as e:
    print(f"Test 10 passed: {e}")

# Test 11 - valid category
try:
    validate_category("Food")
    print("Test 11 passed: Valid category accepted.")
except ValidationError as e:
    print(f"Test 11 failed: {e}")

# Test validate_index

print("\n -------- Validate Index --------")

expenses = [{"title": "Coffee"}, {"title": "Lunch"}, {"title": "Netflix"}]

# Test 12 - valid index

try:
    validate_index(2, expenses)
    print(f"Test 12 passed: Valid index accepted.")
except ValidationError as e:
    print(f"Test 12 failed: {e}")

# Test 13 - index out of range

try:
    validate_index(11, expenses)
except ValidationError as e:
    print(f"Test 13 passed: {e}")

# Test 14 - index zero

try:
    validate_index(0, expenses)
except ValidationError as e:
    print(f"Test 14 passed: {e}")

# Test 15 - negative index
try:
    validate_index(-1, expenses)
except ValidationError as e:
    print(f"Test 15 passed: {e}")

# Test 16 - first valid index

try:
    validate_index(1, expenses)
    print("Test 16 passed: First valid index accepted.")
except ValidationError as e:
    print(f"Test 16 failed: {e}")

# Test 17 - last valid index

try:
    validate_index(len(expenses), expenses)
    print("Test 17 passed: Last valid index accepted.")
except ValidationError as e:
    print(f"Test 17 failed: {e}")

print("\n" + "=" * 50)
print("All validator tests complete!")
print("=" * 50)
