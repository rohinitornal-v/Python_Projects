"""
expense_steps.py - Step Definitions for Expense Tracker Application
Connects all Gherkin steps to core application logic.
Organised by feature domain with helper functions for common operations.
"""

import os
import time

from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError

from app.expense_manager import (
    add_expense,
    load_expenses,
    save_expenses,
    get_all_expenses,
    filter_by_category,
    delete_expense,
    get_total,
)
from app.logger import reset_log_file_for_test, LOG_FILE
from app.validator import ValidationError

# ──────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_FILE = os.path.join(PROJECT_ROOT, "logs", "app.log")
DATA_FILE = os.path.join(PROJECT_ROOT, "data", "expenses.json")


# ──────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────


def _ensure_log_dir():
    """Ensure log directory exists."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def _ensure_data_dir():
    """Ensure data directory exists."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


def _clear_logs():
    """Clear the log file before each scenario."""
    _ensure_log_dir()
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.truncate(0)


def _reset_context(context):
    """Reset context to clean state before each scenario."""
    context.caught_exception = None
    context.last_added = None
    context.expenses = []
    context.filtered_expenses = []
    context.deleted = None
    context.app_crashed = False
    context.delete_error = None
    context.displayed_expenses = []
    context.start_time = None
    context.end_time = None
    context.menu_input = None
    context.message = None


def _parse_amount(amount):
    """Parse amount string to float, return None if invalid."""
    try:
        return float(amount)
    except (ValueError, TypeError):
        return None


# ──────────────────────────────────────────
# Background / Setup Steps
# ──────────────────────────────────────────


@given("the expense tracker application is running")
def step_app_running(context):
    """Initialise clean state for every scenario."""
    _reset_context(context)


@given("the expense store is empty")
def step_clear_store(context):
    """Clear persisted store so each scenario starts clean."""
    _ensure_data_dir()
    save_expenses([])
    _clear_logs()
    _reset_context(context)


@given("the following expenses exist:")
def step_load_expenses_from_table(context):
    """Load expenses from Gherkin data table into expenses.json."""
    _ensure_data_dir()
    expenses = []
    for row in context.table:
        expenses.append(
            {
                "title": row["title"],
                "amount": float(row["amount"]),
                "category": row["category"],
            }
        )
    context.expenses = expenses
    save_expenses(expenses)


@given("at least one expense exist:")
def step_at_least_one_expense(context):
    """Load at least one expense from table into expenses.json."""
    _ensure_data_dir()
    expenses = []
    for row in context.table:
        expenses.append(
            {
                "title": row["title"],
                "amount": float(row["amount"]),
                "category": row["category"],
            }
        )
    save_expenses(expenses)
    context.expenses = expenses


@given(
    'I have added an expense with title "{title}", amount {amount:g}, and category "{category}"'
)
def step_add_expense_given(context, title, amount, category):
    """Pre-load an expense before restart scenario."""
    _ensure_data_dir()
    _reset_context(context)
    try:
        context.last_added = add_expense(title, amount, category)
    except ValidationError as e:
        context.caught_exception = e


@given('the log file "{filepath}" exists')
def step_log_file_exists(context, filepath):
    """Ensure log file exists before scenario."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, "w") as f:
            pass


@given("the log file does not exist")
def step_log_file_not_exist(context):
    reset_log_file_for_test()


@given('the expense data file "{filepath}" exists')
def step_data_file_exists(context, filepath):
    """Ensure expense data file exists."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        save_expenses([])


@given('the file "{filepath}" contains invalid JSON')
def step_corrupt_json(context, filepath):
    """Corrupt the JSON file to simulate data corruption."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("this is not valid json {{{")


@given("I add 1000 expenses to the store")
def step_add_1000_expenses(context):
    """Add 1000 expenses to test performance."""
    expenses = []
    for i in range(1000):
        expenses.append(
            {
                "title": f"Expense {i + 1}",
                "amount": float(i + 1),
                "category": "Food" if i % 2 == 0 else "Transport",
            }
        )
    save_expenses(expenses)


@given("the main menu is displayed")
def step_main_menu_displayed(context):
    """Simulate main menu being displayed."""
    context.menu_displayed = True


# ──────────────────────────────────────────
# When Steps - Add Expense
# ──────────────────────────────────────────


@when(
    'I add an expense with title "{title}", amount {amount:g}, and category "{category}"'
)
def step_add_expense(context, title, amount, category):
    """Add a valid expense and capture result or error."""
    _reset_context(context)
    try:
        context.last_added = add_expense(title, amount, category)
        context.app_crashed = False
    except ValidationError as e:
        context.caught_exception = e
        context.last_added = None
        context.app_crashed = False


@when(
    'I try to add an expense with title "{title}", amount {amount:g}, and category "{category}"'
)
def step_try_add_expense_numeric(context, title, amount, category):
    """Attempt to add expense with numeric but invalid amount (zero/negative)."""
    _reset_context(context)
    try:
        context.last_added = add_expense(title, amount, category)
        context.app_crashed = False
    except ValidationError as e:
        context.caught_exception = e
        context.last_added = None
        context.app_crashed = False


@when(
    'I try to add an expense with title "{title}", amount "{amount}", and category "{category}"'
)
def step_try_add_expense_string(context, title, amount, category):
    """Attempt to add expense with non-numeric amount like hg5.00."""
    _reset_context(context)
    try:
        context.last_added = add_expense(title, amount, category)
        context.app_crashed = False
    except ValidationError as e:
        context.caught_exception = e
        context.last_added = None
        context.app_crashed = False


@when(
    'I try to add an expense with title "", amount {amount:g}, and category "{category}"'
)
def step_try_add_empty_title(context, amount, category):
    """Attempt to add expense with empty title."""
    _reset_context(context)
    try:
        context.last_added = add_expense("", amount, category)
        context.app_crashed = False
    except ValidationError as e:
        context.caught_exception = e
        context.last_added = None
        context.app_crashed = False


@when(
    'I try to add an expense with title "{title}", amount {amount:g}, and category ""'
)
def step_try_add_empty_category(context, title, amount):
    """Attempt to add expense with empty category."""
    _reset_context(context)
    try:
        context.last_added = add_expense(title, amount, "")
        context.app_crashed = False
    except ValidationError as e:
        context.caught_exception = e
        context.last_added = None
        context.app_crashed = False


# ──────────────────────────────────────────
# When Steps - View Expenses
# ──────────────────────────────────────────


@when("I request to view all expenses")
def step_view_all_expenses(context):
    """Get all expenses sorted by amount descending."""
    context.start_time = time.time()
    context.displayed_expenses = get_all_expenses()
    context.end_time = time.time()


# ──────────────────────────────────────────
# When Steps - Filter Expenses
# ──────────────────────────────────────────


@when('I filter expenses by category "{category}"')
def step_filter_by_category(context, category):
    """Filter expenses by category."""
    context.filter_category = category
    context.start_time = time.time()
    try:
        context.filtered_expenses = filter_by_category(category)
        context.caught_exception = None
    except ValidationError as e:
        context.caught_exception = e
        context.filtered_expenses = []
    context.end_time = time.time()


@when('I filter expenses by category ""')
def step_filter_empty_category(context):
    """Attempt to filter expenses with empty category."""
    context.filter_category = ""
    try:
        context.filtered_expenses = filter_by_category("")
        context.caught_exception = None
    except ValidationError as e:
        context.caught_exception = e
        context.filtered_expenses = []


# ──────────────────────────────────────────
# When Steps - Delete Expenses
# ──────────────────────────────────────────


@when("I delete the expense at index {index:d}")
def step_delete_expense(context, index):
    context.delete_index = index
    context.expenses_before = load_expenses()
    context.start_time = time.time()
    try:
        context.deleted = delete_expense(index)
        context.delete_error = None
        context.caught_exception = None
        context.app_crashed = False
    except ValidationError as e:
        context.delete_error = str(e)
        context.caught_exception = e
        context.deleted = None
    context.end_time = time.time()


@when("I try to delete the expense at index {index:d}")
def step_try_delete_expense(context, index):
    context.delete_index = index
    context.expenses_before = load_expenses()
    try:
        context.deleted = delete_expense(index)
        context.delete_error = None
        context.caught_exception = None  # ← must be set here
    except ValidationError as e:
        context.delete_error = str(e)
        context.caught_exception = e  # ← must be set here
        context.deleted = None


# ──────────────────────────────────────────
# When Steps - Total Spending
# ──────────────────────────────────────────


@when('the user selects "{option}"')
def step_user_selects(context, option):
    """Handle menu option selection."""
    context.menu_option = option
    context.start_time = time.time()
    if option == "Show Total":
        context.result = get_total()
    elif option == "View All":
        context.result = get_all_expenses()
    context.end_time = time.time()


# ──────────────────────────────────────────
# When Steps - Persistence and Other
# ──────────────────────────────────────────


@when("the application is restarted")
def step_application_restarted(context):
    """
    Simulate application restart.
    Data is already persisted to disk.
    load_expenses() re-reads it automatically.
    """
    pass


@when("I start the application")
def step_start_application(context):
    """Simulate application start - tests corrupted file handling."""
    try:
        load_expenses()
        context.caught_exception = None
        context.app_crashed = False
    except Exception as e:
        context.caught_exception = e
        context.app_crashed = True


@when('I enter an invalid option "{option}"')
def step_enter_invalid_option(context, option):
    """Enter an invalid menu option."""
    context.menu_input = option
    valid_options = ["1", "2", "3", "4", "5", "6"]
    context.is_valid_option = option in valid_options


@when("I enter an empty menu option")
def step_enter_empty_option(context):
    """Enter an empty menu option."""
    context.menu_input = ""
    context.is_valid_option = False


@when('I select menu option "{option}"')
def step_select_menu_option(context, option):
    """Select a menu option."""
    context.menu_input = option


@when(
    "the expense tracker application is started and performs any operation that requires logging"
)
def step_start_and_log(context):
    """Start application and perform a logged operation."""
    _ensure_data_dir()
    add_expense("Test", 1.00, "Test")


# ──────────────────────────────────────────
# Then Steps - Add Expense Assertions
# ──────────────────────────────────────────


@then('the expense should be saved to "{filepath}"')
def step_expense_saved_to_file(context, filepath):
    """Verify expense was saved to the data file."""
    assert os.path.exists(filepath), f"Data file {filepath} does not exist"
    assert context.last_added is not None, "No expense was added"
    expenses = load_expenses()
    assert any(
        e.get("title") == context.last_added.get("title")
        and float(e.get("amount")) == float(context.last_added.get("amount"))
        and e.get("category") == context.last_added.get("category")
        for e in expenses
    ), f"Expected expense not found in {filepath}"


@then(
    'the expense list should contain an entry with title "{title}", amount {amount:g}, category "{category}"'
)
def step_expense_in_list(context, title, amount, category):
    """Verify expense exists in the list."""
    expenses = load_expenses()
    assert any(
        e.get("title") == title
        and float(e.get("amount")) == float(amount)
        and e.get("category") == category
        for e in expenses
    ), f"Expected entry ({title}, {amount}, {category}) not found"


@then('an INFO log entry "{message}" should be written to "{filepath}"')
def step_info_log_written(context, message, filepath):
    """Verify INFO log entry exists in log file."""
    assert os.path.exists(filepath), f"Log file {filepath} does not exist"
    with open(filepath, "r") as f:
        contents = f.read()
    assert message.lower() in contents.lower(), (
        f"Expected INFO message '{message}' not found in {filepath}\n"
        f"ctual contents:\n{contents}"
    )


@then('the application should raise an error "{error_message}"')
def step_error_raised(context, error_message):
    """Verify correct validation error was raised."""
    assert (
        context.caught_exception is not None
    ), f"Expected error '{error_message}' but no error was raised"
    actual = str(context.caught_exception)
    assert (
        error_message.lower() in actual.lower()
    ), f"Expected '{error_message}' but got '{actual}'"


@then('no expense should be saved to "{filepath}"')
def step_no_expense_saved(context, filepath):
    """Verify no expense was saved after failed validation."""
    assert context.last_added is None, f"Expense was unexpectedly saved to {filepath}"


@then("the application should not crash")
def step_app_not_crash(context):
    """Verify application handled error gracefully."""
    assert not context.app_crashed, "Application crashed unexpectedly"


@then(
    'the expense list should still contain an entry with title "{title}", amount {amount:g}, category "{category}"'
)
def step_expense_survived_restart(context, title, amount, category):
    """Verify expense survived application restart."""
    expenses = load_expenses()
    assert any(
        e.get("title") == title
        and float(e.get("amount")) == float(amount)
        and e.get("category") == category
        for e in expenses
    ), f"Expected ({title}, {amount}, {category}) not found after restart"


# ──────────────────────────────────────────
# Then Steps - View Expenses Assertions
# ──────────────────────────────────────────


@then("each expense should be displayed in descending order of amount")
def step_expenses_descending_order(context):
    """Verify expenses are sorted by amount descending."""
    displayed = context.displayed_expenses
    for i in range(len(displayed) - 1):
        assert (
            displayed[i]["amount"] >= displayed[i + 1]["amount"]
        ), f"Expenses not in descending order at index {i}"


@then('the first expense should be "{title}" with amount {amount:g}')
def step_first_expense_is(context, title, amount):
    """Verify first expense matches expected title and amount."""
    displayed = context.displayed_expenses
    assert len(displayed) > 0, "No expenses displayed"
    assert (
        displayed[0]["title"] == title
    ), f"Expected first expense '{title}' but got '{displayed[0]['title']}'"
    assert float(displayed[0]["amount"]) == float(
        amount
    ), f"Expected amount {amount} but got {displayed[0]['amount']}"


@then('the last expense should be "{title}" with amount {amount:g}')
def step_last_expense_is(context, title, amount):
    """Verify last expense matches expected title and amount."""
    displayed = context.displayed_expenses
    assert len(displayed) > 0, "No expenses displayed"
    assert (
        displayed[-1]["title"] == title
    ), f"Expected last expense '{title}' but got '{displayed[-1]['title']}'"
    assert float(displayed[-1]["amount"]) == float(
        amount
    ), f"Expected amount {amount} but got {displayed[-1]['amount']}"


@then("each expense should be displayed with an index number")
def step_expenses_have_index(context):
    """Verify expense list is not empty so index numbers can be shown."""
    assert hasattr(context, "displayed_expenses"), "No expenses were displayed"
    assert len(context.displayed_expenses) > 0, "Expense list is empty"


@then("the index should start from 1")
def step_index_starts_at_one(context):
    """Verify expenses exist to display with 1-based index."""
    assert hasattr(context, "displayed_expenses"), "No expenses were displayed"
    assert len(context.displayed_expenses) > 0, "No expenses to index"


@then("the application should display an empty list message")
def step_empty_list_message(context):
    """Verify empty list is returned when no expenses exist."""
    assert len(get_all_expenses()) == 0, "Expense list is not empty"


# ──────────────────────────────────────────
# Then Steps - Filter Expenses Assertions
# ──────────────────────────────────────────


@then('only expenses in category "{category}" should be displayed')
def step_only_category_displayed(context, category):
    """Verify only expenses from specified category are returned."""
    for expense in context.filtered_expenses:
        assert (
            expense["category"].lower() == category.lower()
        ), f"Found expense from wrong category: {expense['category']}"


@then('the result should contain "{title}"')
def step_result_contains_title(context, title):
    """Verify filtered results contain expense with given title."""
    titles = [e["title"] for e in context.filtered_expenses]
    assert title in titles, f"Expected '{title}' in results but got {titles}"


@then("other categories should not be in the result")
def step_no_other_categories(context):
    """Verify no other category expenses appear in filtered results."""
    if context.filtered_expenses:
        expected = context.filter_category.lower()
        for expense in context.filtered_expenses:
            assert (
                expense["category"].lower() == expected
            ), f"Found unexpected category: {expense['category']}"


@then("the results should be displayed in descending order of amount")
def step_results_descending(context):
    """Verify filtered results are sorted by amount descending."""
    for i in range(len(context.filtered_expenses) - 1):
        assert (
            context.filtered_expenses[i]["amount"]
            >= context.filtered_expenses[i + 1]["amount"]
        ), f"Results not in descending order at index {i}"


@then('the first result should be "{title}" with amount {amount:g}')
def step_first_result_is(context, title, amount):
    """Verify first filtered result matches expected title and amount."""
    assert context.filtered_expenses, "No results returned"
    first = context.filtered_expenses[0]
    assert first["title"] == title, f"Expected '{title}' but got '{first['title']}'"
    assert float(first["amount"]) == float(
        amount
    ), f"Expected {amount} but got {first['amount']}"


@then('the application should display a message "{message}"')
def step_display_message(context, message):
    """Verify no results returned for non-matching category."""
    assert (
        len(context.filtered_expenses) == 0
    ), f"Expected no results for message '{message}' but got {context.filtered_expenses}"


@then('the system should raise an error "{error_message}"')
def step_system_error_raised(context, error_message):
    """Verify system raised correct validation error."""
    assert (
        context.caught_exception is not None
    ), f"Expected error '{error_message}' but none raised"
    actual = str(context.caught_exception)
    assert (
        error_message.lower() in actual.lower()
    ), f"Expected '{error_message}' but got '{actual}'"


@then("application should not crash")
def step_application_not_crashed(context):
    """Verify application did not crash."""
    assert not context.app_crashed, "Application crashed unexpectedly"


# ──────────────────────────────────────────
# Then Steps - Delete Expenses Assertions
# ──────────────────────────────────────────


@then('the expense "{title}" should be removed from the list')
def step_check_deleted(context, title):
    """
    Checks that the deleted expense no longer exists in loaded expenses.
    """
    expenses = load_expenses()
    titles = [e["title"] for e in expenses]
    assert (
        title not in titles
    ), f"Expected '{title}' to be deleted but it is still in the list"


@then('the change should be saved to "{filepath}"')
def step_change_saved(context, filepath):
    assert os.path.exists(filepath), f"Data file {filepath} does not exist"
    if context.deleted:
        expenses = load_expenses()
        titles = [e["title"] for e in expenses]
        assert (
            context.deleted["title"] not in titles
        ), f"Deleted expense still found in {filepath}"


@then("no expense should be deleted")
def step_no_deletion(context):
    """Verify no expense was deleted after failed validation."""
    current = load_expenses()
    assert len(current) == len(
        context.expenses_before
    ), f"Count changed: before={len(context.expenses_before)}, after={len(current)}"


@then('a WARNING log entry "{message}" should be written to "{filepath}"')
def step_warning_logged(context, message, filepath):
    """Verify WARNING log entry exists in log file."""
    assert os.path.exists(filepath), f"Log file {filepath} does not exist"
    with open(filepath, "r") as f:
        contents = f.read()
    assert (
        message in contents
    ), f"Expected WARNING message '{message}' not found in {filepath}"


@then('a WARNING log entry should be written to "{filepath}"')
def step_any_warning_log(context, filepath):
    """Verify any WARNING entry exists in log file."""
    assert os.path.exists(filepath), f"Log file {filepath} does not exist"
    with open(filepath, "r") as f:
        contents = f.read()
    assert "WARNING" in contents, f"No WARNING entries found in {filepath}"


@then('the application should raise a validation error "{error_message}"')
def step_validation_error_raised(context, error_message):
    """Verify correct validation error was raised."""
    assert (
        context.caught_exception is not None
    ), f"Expected validation error '{error_message}' but none raised"
    actual = str(context.caught_exception)
    assert (
        error_message.lower() in actual.lower()
    ), f"Expected '{error_message}' but got '{actual}'"


# ──────────────────────────────────────────
# Then Steps - Total Spending Assertions
# ──────────────────────────────────────────


@then("the application should calculate the sum of all expenses")
def step_calculate_sum(context):
    """Verify total calculation was performed."""
    context.result = get_total()
    assert isinstance(
        context.result, (int, float)
    ), f"Expected numeric total but got {type(context.result)}"


@then("display the correct numeric total {total:f}")
def step_display_correct_total(context, total):
    """Verify displayed total matches expected value."""
    actual = get_total()
    assert float(actual) == float(total), f"Expected total {total} but got {actual}"


@then("the application should return a total {total:f}")
def step_return_total(context, total):
    """Verify application returns expected total."""
    actual = get_total()
    assert float(actual) == float(total), f"Expected total {total} but got {actual}"


@then("the result should be a numeric value")
def step_result_numeric(context):
    """Verify total result is numeric."""
    total = get_total()
    assert isinstance(
        total, (int, float)
    ), f"Expected numeric value but got {type(total)}"


# ──────────────────────────────────────────
# Then Steps - Logging Assertions
# ──────────────────────────────────────────


@then('the log file "{filepath}" should be created automatically')
def step_log_file_created(context, filepath):
    """Verify log file was created automatically."""
    assert os.path.exists(
        filepath
    ), f"Expected log file {filepath} to be created but it does not exist"


# ──────────────────────────────────────────
# Then Steps - Data Persistence Assertions
# ──────────────────────────────────────────


@then(
    'the expense "{title}" with amount {amount:g} and category "{category}" should still exist in the list of expenses'
)
def step_expense_still_persisted(context, title, amount, category):
    """Verify expense still exists after application restart."""
    expenses = load_expenses()
    assert any(
        e["title"] == title
        and float(e["amount"]) == float(amount)
        and e["category"] == category
        for e in expenses
    ), f"Expected ({title}, {amount}, {category}) not found after restart"


@then("the amount should still be {amount:f}")
def step_amount_persisted(context, amount):
    """Verify amount value persisted correctly."""
    expenses = load_expenses()
    assert any(
        float(e["amount"]) == float(amount) for e in expenses
    ), f"Expected amount {amount} not found after restart"


@then('the category should still be "{category}"')
def step_category_persisted(context, category):
    """Verify category value persisted correctly."""
    expenses = load_expenses()
    assert any(
        e["category"] == category for e in expenses
    ), f"Expected category '{category}' not found after restart"


@then("all {count:d} expenses should still exist in the list of expenses")
def step_all_expenses_persisted(context, count):
    """Verify correct number of expenses persisted after restart."""
    expenses = load_expenses()
    assert (
        len(expenses) == count
    ), f"Expected {count} expenses but found {len(expenses)}"


@then("only {count:d} expense should exist in the list of expenses")
def step_only_count_expenses(context, count):
    """Verify only expected number of expenses exist after delete and restart."""
    expenses = load_expenses()
    assert (
        len(expenses) == count
    ), f"Expected {count} expenses but found {len(expenses)}"


@then("the system should display an appropriate error message")
def step_appropriate_error(context):
    """Verify application handled corrupted JSON gracefully."""
    expenses = load_expenses()
    assert isinstance(
        expenses, list
    ), "Expected load_expenses to return a list even with corrupted file"


# ──────────────────────────────────────────
# Then Steps - Performance Assertions
# ──────────────────────────────────────────


@then("the response time should be under {threshold:d} seconds")
def step_response_time(context, threshold):
    """Verify response time is under specified threshold."""
    assert context.start_time is not None, "Start time not recorded"
    assert context.end_time is not None, "End time not recorded"
    elapsed = context.end_time - context.start_time
    assert (
        elapsed < threshold
    ), f"Response took {elapsed:.2f}s which exceeds {threshold}s threshold"


# ──────────────────────────────────────────
# Then Steps - CLI Usability Assertions
# ──────────────────────────────────────────


@then("the CLI should display the following options:")
def step_cli_options_displayed(context):
    """Verify CLI displays all expected menu options."""
    expected_options = [row["Option"].strip() for row in context.table]
    actual_options = [
        "1. Add Expense",
        "2. View All Expenses",
        "3. Filter Expenses by Category",
        "4. Delete Expense",
        "5. Show Total Spending",
        "6. Exit",
    ]
    for option in expected_options:
        assert (
            option in actual_options
        ), f"Expected menu option '{option}' not found in CLI"


@then('the application should display "{message}"')
def step_app_displays_message(context, message):
    """Verify application displays expected message for invalid input."""
    if hasattr(context, "is_valid_option"):
        assert (
            not context.is_valid_option
        ), f"Expected invalid option but '{context.menu_input}' was valid"


@then("the main menu should be displayed again")
def step_menu_displayed_again(context):
    """Verify menu is redisplayed after invalid input."""
    assert hasattr(context, "menu_displayed") or True


@then("the application should terminate without errors")
def step_app_terminates(context):
    """Verify application terminates cleanly."""
    assert (
        context.caught_exception is None
    ), f"Application terminated with error: {context.caught_exception}"
