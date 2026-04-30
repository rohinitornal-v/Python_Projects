# Expense Tracker Test Runner

.PHONY: run unit bdd integration performance coverage fast full clean

# Run application
run:
	python3 main.py

# -----------------------------
# Unit Tests (Fast)
# -----------------------------
unit:
	pytest tests/test_validator.py tests/test_expense_manager.py -v

# -----------------------------
# BDD Tests
# -----------------------------
bdd:
	behave

bdd-verbose:
	behave -v

bdd-feature:
	behave features/01_add_expenses.feature

# -----------------------------
# Integration Tests
# -----------------------------
integration:
	pytest tests/test_integration.py -v

# -----------------------------
# Performance Tests (Slow)
# -----------------------------
performance:
	pytest tests/test_performance.py -v -s

# -----------------------------
# Fast Tests (Run Always)
# -----------------------------
fast:
	pytest tests/test_validator.py tests/test_expense_manager.py -v

# -----------------------------
# Full Tests (Before Release)
# -----------------------------
full:
	pytest tests/ --ignore=tests/test_performance.py --cov=app --cov-report=term-missing

# -----------------------------
# Coverage
# -----------------------------
coverage:
	pytest tests/ --cov=app --cov-report=term-missing

# -----------------------------
# Run Everything
# -----------------------------
all:
	make fast
	make integration
	make bdd
	make coverage

# -----------------------------
# Clean cache
# -----------------------------
clean:
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf .coverage
