# Expense tracker CLI

# Overview

A command-line expense tracking application built using Python,
demonstrating BDD methodology with Cucumber/Gherkin (behave).
This project was built following outside-in BDD development,
written from the perspective of both a Junior Developer and QA/SDET.

# Author
Rohini

# Tech Stack
Python 3.9+
behave (BDD framework - Python Cucumber equivalent)
pytest (unit testing)

# Project Structure

expense-tracker/
│
├── app/                         # Core application logic
│   ├── __init__.py
│   ├── expense_manager.py       # Business logic
│   └── logger.py                # Logging setup
│   ├── validator.py             # Input validation
|
├── features/                    # BDD feature files
│   ├── 01_add_expenses.feature
│   ├── 02_view_expenses.feature
│   ├── 03_filter_expenses.feature
│   ├── 04_delete_expenses.feature
│   ├── 05_total_spending.feature
│   ├── 06_logging.feature
│   ├── 07_data_persistence.feature
│   ├── 08_performance.feature
│   ├── 09_cli_usability.feature
│   └── steps/
│       └── expense_steps.py     # Step definitions
│
├── tests/                       # Unit tests
│   ├── __init__.py
│   └── test_validator_quick.py
│
├── docs/                        # Project documentation
│   └── requirements_bdd.md      # BDD requirements document
│
├── data/                        # Data storage
│   └── expenses.json            # Expense data
│
├── logs/                        # Application logs
│   └── app.log                  # Log file
│
├── main.py                      # CLI entry point
├── conftest.py                  # pytest path configuration
├── behave.ini                   # behave configuration
└── README.md

# BDD approach

This project follows outside-in BDD development:

Requirements (docs/requirements_bdd.md)
        ↓
Feature Files (features/*.feature)
        ↓
Step Definitions (features/steps/expense_steps.py)
        ↓
Core Logic (app/)
        ↓
Unit Tests (tests/)
        ↓
CLI (main.py)

# Feature

Add expenses with title, amount and category
View all expenses sorted by amount descending
Filter expenses by category (case-insensitive)
Delete expenses by index
Show total spending
Data persistence via JSON (data/expenses.json)
Full logging of all operations (logs/app.log)
Input validation with clear error messages
