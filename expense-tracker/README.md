# Expense tracker CLI

# Overview

A command-line expense tracking application built using Python,
demonstrating BDD methodology with Cucumber/Gherkin (behave).
This project was built following outside-in BDD development,
written from the perspective of both a Junior Developer and QA/SDET.

# Author
Rohini - QA professional transitioning to SDET, Junior Python programmer
Roles played: Business Analyst, Junior developer, QA/SDET

# Project Purpose
This project was built as a portfolio piece to demonstrate SDET skills including:
- BDD methodology with Gherkin/Cucumber(behave)
- Outside-in-test-driven development
- Unit testing with pytest
- Clean code architecture
- Professional Git workflow
- Real-world Agile practices

# Tech Stack
Python 3.9+ : Core language
behave : BDD framework - Python Cucumber equivalent
pytest : Unit testing
pytest-cov : Test coverage reporting
JSON : Data persistence
logging : Application logging

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
(QA/SDET)
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
(Developer/SDET)
│   ├── __init__.py
|   └── conftest.py
│   └── test_validator_quick.py  # Validator unit tests
│   └── test_expense_manager.py  # Business logic unit test
|   └──test_data
       └── test_app-log
       └── test_expenses.json
│
├── docs/                        # Project documentation
│   └── requirements_bdd.md      # BDD requirements document
│
├── data/                        # Data storage
│   └── expenses.json            # Expense data
│   └── test_expenses.json       # Test data (isolated)
│
├── logs/                        # Application logs
│   └── app.log                  # Log file
│   └── test_app.log             # Test log (isolated)
│
├── main.py                      # CLI entry point
├── conftest.py                  # pytest path configuration
├── behave.ini                   # behave configuration
└── README.md

# BDD Development approach

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

# Feature in Version 1.0

1. Add expenses with title, amount and category
2. View all expenses sorted by amount descending
3. Filter expenses by category (case-insensitive)
4. Delete expenses by index
5. Show total spending
6. Data persistence via JSON (data/expenses.json)
7. Full logging of all operations (logs/app.log)
8. Input validation with clear error messages

# Run Coverage Report

pytest tests/ --cov=app --cov-report=term-missing

# Getting Started

# Pre-requisites

Python 3.9+

# Installation

# Clone the repository
git clone https://github.com/yourusername/expense-tracker.git

# Navigate to project folder
cd expense-tracker

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows

# Install dependencies
pip install behave pytest pytest-cov

# Run the application

python3 main.py

# Run BDD Tests

# Run all feature files
behave

# Run a specific feature file
behave features/01_add_expenses.feature

# Run with verbose output
behave -v

# Run Unit Tests

# Run all unit tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_validator.py -v
pytest tests/test_expense_manager.py -v

# Architecture

Separation of Concerns

main.py              ← CLI layer (user interaction only)
    ↓ calls
app/expense_manager.py  ← Business logic layer
    ↓ calls
app/validator.py        ← Validation layer
app/logger.py           ← Logging layer
    ↓ reads/writes
data/expenses.json      ← Data layer
logs/app.log            ← Log layer

# Test Isolation

Tests use separate data file to avoid interfering with production data
Production:  data/expenses.json    logs/app.log
Tests:       data/test_expenses.json  logs/test_app.log

Controlled via environment variables in conftest.py

# Learning Journey

This project demonstrates growth across multiple roles:
Role                            Skills Demonstrated
--------------------------------------------------------------------------------------------------------
Business Analyst        Requirements gathering, BDD documentation, acceptance criteria
Developer               Python OOP, file I/O, JSON, logging, CLI design, clean architecture
QA/SDET                 Gherkin writing, BDD with behave, step definitions, pytest, test isolation
--------------------------------------------------------------------------------------------------------

# License

This project is for portfolio and learning purposes.
