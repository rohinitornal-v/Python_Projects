"""Step Definitions"""

from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError
import os

# Connect to core application logic
from app.expense_manager import (
    add_expense,
    load_expenses,
    save_expenses,
)
from app.validator import ValidationError
from app.logger import LOG_FILE

# -------------------------------
# Background Steps: Add Expense
# -------------------------------


@given("the expense tracker application is running")
def step_impl(context):
    # Initialise clean state for every scenario
    context.error = None
    context.last_expense = None


@given("the expense store is empty")
def step_impl(context):
    # Clear persisted store so each scenario starts clean
    try:
        save_expenses([])
    except Exception:
        # fallback: remove file if exists
        data_file = "data/expenses.json"
        if os.path.exists(data_file):
            os.remove(data_file)


# --------------------------------
# When Steps - Add Valid Expense
# --------------------------------


@when(
    'I add an expense with title "{title}", amount {amount:f}, and category "{category}"'
)
def step_impl(context, title, amount, category):
    # Stores values in context so Then steps can use them
    context.title = title
    context.amount = amount
    context.category = category
    context.exception = None
    try:
        context.last_expense = add_expense(title, amount, category)
    except ValidationError as e:
        context.exception = e
        context.last_expense = None


# @then('the expense should be saved to "{filepath}"')
# def step_impl(context, filepath):
# raise StepNotImplementedError(
#'Then the expense should be saved to "data/expenses.json"'
# )


# ----------------------------------
# When Steps - Add InValid Expense
# ----------------------------------


@when(
    'I try to add an expense with title "{title}", amount {amount:f}, and category "{category}"'
)
def step_impl(context, title, amount, category):
    # Attempt to add and capture validation errors (zero/negative amounts)
    context.title = title
    context.amount = amount
    context.category = category
    context.exception = None
    try:
        context.last_expense = add_expense(title, amount, category)
    except ValidationError as e:
        context.exception = e
        context.last_expense = None


@when(
    'I try to add an expense with title "{title}", amount {amount}, and category "{category}"'
)
def step_impl(context, title, amount, category):
    # Handles non-numeric amounts like "hg5.00"
    # # amount is captured as string because it is not a valid number
    context.title = title
    context.amount = amount
    context.category = category
    context.exception = None
    try:
        context.last_expense = add_expense(title, amount, category)
    except ValidationError as e:
        context.exception = e
        context.last_expense = None


# ──────────────────────────────────────────
# When Steps - Empty Title and Category
# ──────────────────────────────────────────


@when(
    'I try to add an expense with title "", amount {amount:f}, and category "{category}"'
)
def step_impl(context, amount, category):
    # Handles empty title case
    context.title = ""
    context.amount = amount
    context.category = category
    context.exception = None
    try:
        context.last_expense = add_expense("", amount, category)
    except ValidationError as e:
        context.exception = e
        context.last_expense = None


@when(
    'I try to add an expense with title "{title}", amount {amount:f}, and category ""'
)
def step_impl(context, title, amount):
    # Handles empty category case
    context.title = title
    context.amount = amount
    context.category = ""
    context.exception = None
    try:
        context.last_expense = add_expense(title, amount, "")
    except ValidationError as e:
        context.exception = e
        context.last_expense = None


# ──────────────────────────────────────────
# Given Steps - Persistence
# ──────────────────────────────────────────


@given(
    'I have added an expense with title "{title}", amount {amount:f}, and category "{category}"'
)
def step_impl(context, title, amount, category):
    # Pre-loads an expense before restart scenario
    context.title = title
    context.amount = amount
    context.category = category
    context.last_expense = {
        "title": title,
        "amount": amount,
        "category": category,
    }
    # Persist using core logic
    try:
        add_expense(title, amount, category)
    except ValidationError:
        # If validation fails here the feature is mis-specified
        pass


@when("the application is restarted")
def step_impl(context):
    # For our simple persistence model, restarting does nothing special because
    # data is read from disk on demand; we can clear any in-memory caches if needed.
    # No-op here.
    pass


# ──────────────────────────────────────────
# Then Steps - Happy Path Assertions
# ──────────────────────────────────────────


@then('the expense should be saved to "{filepath}"')
def step_impl(context, filepath):
    # Verify the persisted file contains an expense matching last_expense
    assert os.path.exists(filepath), f"Data file {filepath} does not exist"
    expenses = load_expenses()
    assert any(
        e.get("title") == context.last_expense.get("title")
        and float(e.get("amount")) == float(context.last_expense.get("amount"))
        and e.get("category") == context.last_expense.get("category")
        for e in expenses
    ), f"Expected expense not found in {filepath}"


@then(
    'the expense list should contain an entry with title "{title}", amount {amount:f}, category "{category}"'
)
def step_impl(context, title, amount, category):
    expenses = load_expenses()
    assert any(
        e.get("title") == title
        and float(e.get("amount")) == float(amount)
        and e.get("category") == category
        for e in expenses
    ), f"Expected entry ({title}, {amount}, {category}) not found"


@then('an INFO log entry "{message}" should be written to "{filepath}"')
def step_impl(context, message, filepath):
    assert os.path.exists(filepath), f"Log file {filepath} does not exist"
    with open(filepath, "r") as fh:
        contents = fh.read()
    assert (
        message in contents
    ), f"Expected log message '{message}' not found in {filepath}"


# ──────────────────────────────────────────
# Then Steps - Validation Error Assertions
# ──────────────────────────────────────────


@then('the application should raise an error "{error_message}"')
def step_impl(context, error_message):
    assert getattr(context, "exception", None) is not None, "No exception was raised"
    actual = str(context.exception)
    # allow partial matches and ignore punctuation/case
    assert (
        error_message.lower() in actual.lower()
    ), f"Expected error '{error_message}' but got '{actual}'"


@then('no expense should be saved to "{filepath}"')
def step_impl(context, filepath):
    # Verify that either the file doesn't exist or it does not contain the last_expense
    if not os.path.exists(filepath):
        return
    expenses = load_expenses()
    if getattr(context, "last_expense", None) is None:
        # nothing was added
        return
    assert not any(
        e.get("title") == context.last_expense.get("title")
        and float(e.get("amount")) == float(context.last_expense.get("amount"))
        and e.get("category") == context.last_expense.get("category")
        for e in expenses
    ), f"Unexpected expense found in {filepath}"


@then("the application should not crash")
def step_impl(context):
    # Will verify application handled error gracefully and is still running
    raise StepNotImplementedError(
        "needs core logic to verify if application is still running"
    )


# ──────────────────────────────────────────
# Then Steps - Persistence Assertions
# ──────────────────────────────────────────


@then(
    'the expense list should still contain an entry with title "{title}", amount {amount:f}, category "{category}"'
)
def step_impl(context, title, amount, category):
    # Will verify expense survived application restart
    raise StepNotImplementedError(
        "needs core logic to verify if expense survived application restart"
    )


# ---------------------------------
# Background Steps: View Expense
# ---------------------------------


@given("the following expenses exist:")
def step_impl(context):
    # Loads the expense table from the feature file into context
    # context.table contains the rows from the Background table in the feature file
    context.expenses = []
    for row in context.table:
        context.expenses.append(
            {
                "title": row["title"],
                "amount": float(row["amount"]),
                "category": row["category"],
            }
        )
    # Will add expenses to expenses.json when core logic is implemented


# ---------------------------------
# When Steps: View Expense
# ---------------------------------


@when("I request to view all expenses")
def step_impl(context):
    # will get all expenses from the application when core logic is implemented
    raise StepNotImplementedError(
        "needs core logic to get all expenses from application"
    )


# ---------------------------------
# Then Steps: View Expense
# ---------------------------------


@then("each expense should be displayed in descending order of amount")
def step_impl(context):
    # Will verify expenses are sorted by amount descending
    raise StepNotImplementedError(
        "needs core logic to verify sort order of displayed expenses"
    )


@then('the first expense should be "{title}" with amount {amount:f}')
def step_impl(context, title, amount):
    # Will verify first expense in list matches expected title and amount
    raise StepNotImplementedError(
        "needs core logic to verify first expense matches expected title and amount"
    )


@then('the last expense should be "{title}" with amount {amount:f}')
def step_impl(context, title, amount):
    # Will verify last expense in list matches expected title and amount
    raise StepNotImplementedError(
        "needs core logic to verify last expense matches expected title and amount"
    )


@then("each expense should be displayed with an index number")
def step_impl(context):
    # Will verify each displayed expense has an index number
    raise StepNotImplementedError(
        "needs core logic to verify each displayed expense has an index number"
    )


@then("the index should start from 1")
def step_impl(context):
    # Will verify index numbers start from 1 not 0 or some other number
    raise StepNotImplementedError(
        "needs core logic to verify index numbers start from 1"
    )


@then("the application should display an empty list message")
def step_impl(context):
    # Will verify system displays appropriate message when no expenses exist
    raise StepNotImplementedError(
        "needs core logic to verify empty list message is displayed"
    )


# -----------------------------------------------
# Background Steps: Filter Expenses by Category
# -----------------------------------------------


@when('I filter expenses by category "{category}"')
def step_impl(context, category):
    # Stores category in context so Then steps can use it
    context.filter_category = category
    # Will filter expenses by category when core logic is implemented


@when('I filter expenses by category ""')
def step_impl(context):
    # Handles empty category filter case
    context.filter_category = ""
    context.error = "Category cannot be empty"


# ──────────────────────────────────────────
# Then Steps - Filter Expenses
# ──────────────────────────────────────────


@then('only expenses in category "{category}" should be displayed')
def step_impl(context, category):
    # Will verify only expenses with specified category are displayed
    raise StepNotImplementedError(
        "needs core logic to verify only expenses with empty category are displayed"
    )


@then('the result should contain "{title}"')
def step_impl(context, title):
    # Will verify filtered results contain expected title
    raise StepNotImplementedError(
        "needs core logic to verify filtered results contain expected title"
    )


@then("other categories should not be in the result")
def step_impl(context):
    # Will verify filtered results do not contain expenses from other categories
    raise StepNotImplementedError(
        "needs core logic to verify filtered results do not contain expenses from other categories"
    )


@then("the results should be displayed in descending order of amount")
def step_impl(context):
    # Will verify filtered results are sorted by amount descending
    raise StepNotImplementedError(
        "needs core logic to verify sort order of filtered results"
    )


@then('the first result should be "{title}" with amount {amount:f}')
def step_impl(context, title, amount):
    # Will verify first expense in filtered results matches expected title and amount
    raise StepNotImplementedError(
        "needs core logic to verify first expense in filtered results matches expected title and amount"
    )


@then('the application should display a message "{message}"')
def step_impl(context, message):
    # Will verify system displays appropriate message when no expenses match filter
    raise StepNotImplementedError(
        "needs core logic to verify no results message is displayed"
    )


# ------------------------------
# When Steps - Delete Expenses
# ------------------------------


@when("I delete the expense at index {index:d}")
def step_impl(context, index):
    # Stores index in context so Then steps can use it
    context.delete_index = index
    # Will delete expense at specified index when core logic is implemented
    raise StepNotImplementedError(
        "needs core logic to delete expense at specified index"
    )


@when("I try to delete the expense at index {index:d}")
def step_impl(context, index):
    # Handles delete attempt when store is empty or index is out of bounds
    context.delete_index = index
    context.error = "No expenses found"
    # Will attempt to delete expense at specified index and handle error when store is empty or index is invalid
    raise StepNotImplementedError(
        "needs core logic to attempt delete and handle error for empty store or invalid index"
    )


# ------------------------------
# Then Steps - Delete Expenses
# ------------------------------


@then('the expense "{title}" should be removed from the list')
def step_impl(context, title):
    # Will verify expense with specified title is no longer in the list after deletion
    raise StepNotImplementedError(
        "needs core logic to verify expense with specified title is removed from list"
    )


@then('the change should be saved to "{filepath}"')
def step_impl(context, filepath):
    # Will verify change persisted to expenses.json
    raise StepNotImplementedError(
        "needs core logic to verify change is saved to specified file"
    )


@then("no expense should be deleted")
def step_impl(context):
    # Will verify no expenses were deleted when delete attempt failed
    raise StepNotImplementedError("needs core logic to verify no expenses were deleted")


@then('a WARNING log entry "{message}" should be written to "{filepath}"')
def step_impl(context, message, filepath):
    # Will verify logs/app.log contains the WARNING message for failed delete attempt
    raise StepNotImplementedError(
        "needs core logic to verify if WARNING log entry is written to file"
    )


@then('a WARNING log entry should be written to "{filepath}"')
def step_impl(context, filepath):
    # Will verify any WARNING message written to logs/app.log
    raise StepNotImplementedError(
        "needs core logic to verify if WARNING log entry is written to file"
    )


@then('the application should raise a validation error "{error_message}"')
def step_impl(context, error_message):
    # Will verify correct validation error message is raised for failed delete attempt
    raise StepNotImplementedError(
        "needs core logic to verify if correct validation error message is raised"
    )


# ──────────────────────────────────────────
# Given Steps - Total Spending
# ──────────────────────────────────────────


@given("at least one expense exist:")
def step_impl(context):
    # Loads the expense table from the feature file into context
    context.expenses = []
    for row in context.table:
        context.expenses.append(
            {
                "title": row["title"],
                "amount": float(row["amount"]),
                "category": row["category"],
            }
        )
    # Will add expenses to expenses.json when core logic is implemented


# ──────────────────────────────────────────
# When Steps - Total Spending
# ──────────────────────────────────────────


@when('the user selects "{option}"')
def step_impl(context, option):
    # # Captures menu option selected by user
    # Works for "Show Total", "View All" etc
    context.menu_option = option


# ──────────────────────────────────────────
# Then Steps - Total Spending
# ──────────────────────────────────────────


@then("the application should calculate the sum of all expenses")
def step_impl(context):
    # Will calculate total of all expenses when core logic is implemented
    raise StepNotImplementedError("needs core logic to calculate total of all expenses")


@then("display the correct numeric total {total:f}")
def step_impl(context, total):
    # Will verify displayed total matches expected total
    raise StepNotImplementedError(
        "needs core logic to verify displayed total matches expected total"
    )


@then("the application should return a total {total:f}")
def step_impl(context, total):
    # Will verify application returns expected total when no expenses exist
    raise StepNotImplementedError(
        "needs core logic to verify application returns expected total when no expenses exist"
    )


@then("the result should be a numeric value")
def step_impl(context):
    # Will verify total returned is a numeric value and not a string or some other type
    raise StepNotImplementedError(
        "needs core logic to verify total returned is a numeric value"
    )


# ──────────────────────────────────────────
# Background Steps - Logging
# ──────────────────────────────────────────


@given('the log file "{filepath}" exists')
def step_impl(context, filepath):
    # Will verify log file exists before each scenario
    raise StepNotImplementedError(
        "needs core logic to verify log file exists before each scenario"
    )


# ──────────────────────────────────────────
# Given Steps - Log File Creation
# ──────────────────────────────────────────


@given("the log file does not exist")
def step_impl(context, filepath):
    # Will verify log file does not exist before log creation scenario
    raise StepNotImplementedError(
        "needs core logic to verify log file does not exist before log creation scenario"
    )


# ──────────────────────────────────────────
# When Steps - Log File Creation
# ──────────────────────────────────────────


@when(
    "the expense tracker application is started and performs any operation that requires logging"
)
def step_impl(context):
    # Simulates starting the application and performing an operation that triggers logging (e.g. adding an expense)
    raise StepNotImplementedError(
        "needs core logic to simulate starting application and performing operation that triggers logging"
    )


# ──────────────────────────────────────────
# Then Steps - Log File Creation
# ──────────────────────────────────────────


@then('the log file "{filepath}" should be created automatically')
def step_impl(context, filepath):
    # Will verify the log file is created automatically
    raise StepNotImplementedError(
        "needs core logic to verify log file is created automatically"
    )


# ──────────────────────────────────────────
# Background Steps - Data Persistence
# ──────────────────────────────────────────


@given('the expense data file "{filepath}" exists')
def step_impl(context, filepath):
    # WILL verify expenses.json exists before each scenario
    raise StepNotImplementedError(
        "needs core logic to verify expenses.json exists before each scenario"
    )


# ──────────────────────────────────────────
# Then Steps - Data Persistence
# ──────────────────────────────────────────


@then(
    'the expense "{title}" with amount {amount:f} and category "{category}" should still exist in the list of expenses'
)
def step_impl(context, title, amount, category):
    # Will verify the expense survived application restart
    raise StepNotImplementedError(
        "needs core logic to verify expense with specified title, amount and category still exists in list of expenses after application restart"
    )


@then("the amount should still be {amount:f}")
def step_impl(context, amount):
    # Will verify amount value persisted correctly
    raise StepNotImplementedError(
        "needs core logic to verify amount value persisted correctly after application restart"
    )


@then('the category should still be "{category}"')
def step_impl(context, category):
    # Will verify category value persisted correctly
    raise StepNotImplementedError(
        "needs core logic to verify category value persisted correctly after application restart"
    )


@then("all {count:d} expenses should still exist in the list of expenses")
def step_impl(context, count):
    # Will verify correct number of expenses persisted after restart
    raise StepNotImplementedError(
        "needs core logic to verify correct number of expenses persisted after application restart"
    )


@then("only {count:d} expense should exist in the list of expenses")
def step_impl(context, count):
    # Will verify correct number of expenses after delete and restart
    raise StepNotImplementedError(
        "needs core logic to verify correct number of expenses persisted after application restart when some expenses were deleted before restart"
    )


# ──────────────────────────────────────────
# Given, When, Then Steps - Error Handling
# ──────────────────────────────────────────


@given('the file "{filepath}" contains invalid JSON')
def step_impl(context, filepath):
    # Will corrupt expenses.json to simulate corrupted file
    raise StepNotImplementedError(
        "needs core logic to corrupt expenses.json to simulate corrupted file scenario"
    )


@when("I start the application")
def step_impl(context):
    # Will simulate application start
    raise StepNotImplementedError(
        "needs core logic to simulate application start for corrupted file scenario"
    )


@then("the system should display an appropriate error message")
def step_impl(context):
    # Will verify appropriate error message displayed
    raise StepNotImplementedError(
        "needs core logic to verify appropriate error message is displayed for corrupted file scenario"
    )


# ──────────────────────────────────────────
# Given Steps - Performance
# ──────────────────────────────────────────


@given("I add 1000 expenses to the store")
def step_impl(context):
    # Will generate and add 1000 expenses to expenses.json
    # Used to test performance under load
    raise StepNotImplementedError(
        "needs core logic to generate and add 1000 expenses to expenses.json for performance testing"
    )


# @then step will check elapsed time:
@then("the response time should be under {threshold:d} seconds")
def step_impl(context, threshold):
    # Will verify response time is under 2 seconds specified threshold
    raise StepNotImplementedError(
        "needs core logic to measure and verify response time is under specified threshold for performance testing"
    )


# ──────────────────────────────────────────
# Given Steps - CLI Usability
# ──────────────────────────────────────────


@given("the main menu is displayed")
def step_impl(context):
    # Will simulate main menu being displayed when application starts
    raise StepNotImplementedError(
        "needs core logic to simulate main menu being displayed on application start"
    )


@then("the CLI should display the following options:")
def step_impl(context):
    # context.table contains the expected menu options
    # Will verify each option is displayed in the CLI
    raise StepNotImplementedError(
        "needs core logic to verify each expected menu option is displayed in the CLI"
    )


# ──────────────────────────────────────────
# When Steps - Invalid Input
# ──────────────────────────────────────────


@when('I enter an invalid option "{option}"')
def step_impl(context, option):
    # Captures the invalid option entered by the user in context
    context.menu_input = option


@when("I enter an empty menu option")
def step_impl(context):
    # Stores empty string as menu input
    context.menu_input = ""


@when('I select menu option "{option:d}"')
def step_impl(context):
    # Stores selected menu option in context
    context.menu_input = option


# ──────────────────────────────────────────
# Then Steps - Invalid Input Handling
# ──────────────────────────────────────────


@then('the application should display "{message}"')
def step_impl(context, message):
    raise StepNotImplementedError(
        "needs core logic to verify application displays expected message for invalid input"
    )


@then("the main menu should be displayed again")
def step_impl(context):
    # Will verify menu is redisplayed after invalid input
    raise StepNotImplementedError(
        "needs core logic to verify main menu is displayed again after invalid input"
    )


# ──────────────────────────────────────────
# Then Steps - Exit
# ──────────────────────────────────────────


@then("the application should terminate without errors")
def step_impl(context):
    # Will verify application exits cleanly with no exceptions
    raise StepNotImplementedError(
        "needs core logic to verify application exits cleanly with no exceptions"
    )
