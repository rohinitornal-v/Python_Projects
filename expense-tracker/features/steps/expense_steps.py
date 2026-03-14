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
