"""Step Definitions"""

from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError

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
    # Will clear expenses.json when core logic is implemented
    raise StepNotImplementedError("need core logic to clear expense store")


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
    context.last_expense = {
        "title": title,
        "amount": amount,
        "category": category,
    }


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
    # Handles numeric amounts that are invalid (zero, negative)
    context.title = title
    context.amount = amount
    context.category = category
    context.error = "Amount must be greater than 0"


@when(
    'I try to add an expense with title "{title}", amount {amount}, and category "{category}"'
)
def step_impl(context, title, amount, category):
    # Handles non-numeric amounts like "hg5.00"
    # # amount is captured as string because it is not a valid number
    context.title = title
    context.amount = amount
    context.category = category
    context.error = "Amount must be a valid number"


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
    context.error = "Title cannot be empty"


@when(
    'I try to add an expense with title "{title}", amount {amount:f}, and category ""'
)
def step_impl(context, title, amount):
    # Handles empty category case
    context.title = title
    context.amount = amount
    context.category = ""
    context.error = "Category cannot be empty"


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
    # Will add expense to expenses.json when core logic is implemented


@when("the application is restarted")
def step_impl(context):
    # Simulates application restart when core logic is implemented (e.g. reloading expenses from file)
    raise StepNotImplementedError("needs core logic to simulate application restart")


# ──────────────────────────────────────────
# Then Steps - Happy Path Assertions
# ──────────────────────────────────────────


@then('the expense should be saved to "{filepath}"')
def step_impl(context, filepath):
    # Will verify if expense is saved to expenses.json when core logic is implemented
    raise StepNotImplementedError(
        "needs core logic to verify if expense is saved to file"
    )


@then(
    'the expense list should contain an entry with title "{title}", amount {amount:f}, category "{category}"'
)
def step_impl(context, title, amount, category):
    # Will verify if expense list contains the expected entry when core logic is implemented
    raise StepNotImplementedError(
        "needs core logic to verify if expense list contains expected entry"
    )


@then('an INFO log entry "{message}" should be written to "{filepath}"')
def step_impl(context, message, filepath):
    # Will verify logs/app.log contains the INFO message
    raise StepNotImplementedError(
        "needs core logic to verify if INFO log entry is written to file"
    )


# ──────────────────────────────────────────
# Then Steps - Validation Error Assertions
# ──────────────────────────────────────────


@then('the application should raise an error "{error_message}"')
def step_impl(context, error_message):
    # Will verify correct error message is raised
    raise StepNotImplementedError(
        "needs core logic to verify if correct error message is raised"
    )


@then('no expense should be saved to "{filepath}"')
def step_impl(context, filepath):
    # Will verify expenses.json is not modified
    raise StepNotImplementedError(
        "needs core logic to verify if no expense is saved to file"
    )


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


@then("the system should display an empty list message")
def step_impl(context):
    # Will verify system displays appropriate message when no expenses exist
    raise StepNotImplementedError(
        "needs core logic to verify empty list message is displayed"
    )
