"""Step Definitions"""

from behave import given, when, then
from behave.api.pending_step import StepNotImplementedError


@given("the expense tracker application is running")
def step_impl(context):
    raise StepNotImplementedError("Given the expense tracker application is running")


@given("the expense store is empty")
def step_impl(context):
    raise StepNotImplementedError("Given the expense store is empty")


@when(
    'I add an expense with title "{title}", amount {amount:f}, and category "{category}"'
)
def step_impl(context, title, amount, category):
    context.title = title
    context.amount = amount
    context.category = category


@then('the expense should be saved to "{filepath}"')
def step_impl(context, filepath):
    raise StepNotImplementedError(
        'Then the expense should be saved to "data/expenses.json"'
    )


@then(
    'the expense list should contain an entry with title "{title}", amount {amount:f}, category "{category}"'
)
def step_impl(context, title, amount, category):
    raise StepNotImplementedError(
        'Then the expense list should contain an entry with title "{title}", amount {amount:f}, category "{category}"'
    )


@then('an INFO log entry "{message}" should be written to "{filepath}"')
def step_impl(context, message, filepath):
    raise StepNotImplementedError(
        'Then an INFO log entry "{message}" should be written to "{filepath}"'
    )
