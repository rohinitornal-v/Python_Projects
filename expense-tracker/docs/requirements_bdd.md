# Expense Tracker CLI
## BDD requirements document
Author: Rohini
Version: 1.0

## Version History
Version       Date            Changes
------------------------------------------------------------------------------------------------
  1.0         April-2026     Initial release — Add, View, Filter, Delete, Total

------------------------------------------------------------------------------------------------

# Feature 1 : Add Expenses
As a user
I want to add a new expense
So that I can track my spending

## Scenario: Add valid expense
Given the application is running
When the user enters a valid title, amount, and category
# Expense Tracker — BDD Requirements
Author: Rohini
Version: 1.0

The following Gherkin scenarios capture the behaviour of the Expense Tracker CLI.

```gherkin
Feature 1: Add expenses
    In order to track spending
    As a user
    I want to add expenses with a title, amount and category

    Background:
        Given the application is running

    Scenario: Add a valid expense
        When I add an expense with title "Lunch", amount 12.50 and category "Food"
        Then the expense is saved
        And the expense appears in the expense list
        And the expense persists in "data/expenses.json"
        And an INFO log entry is created

    Scenario Outline: Reject invalid expense inputs
        When I add an expense with title "<title>", amount <amount> and category "<category>"
        Then the expense is not saved
        And an error message "<error>" is shown

        Examples:
            | title | amount | category  | error                             |
            | ""    | 10     | Food      | Title cannot be empty             |
            | Tea   | 0      | Beverages | Amount must be greater than 0     |
            | Bus   | -5     | Transport | Amount must be greater than 0     |
            | Cake  | abc    | Food      | Amount must be numeric            |
            | Cake  | 5      | ""        | Category cannot be empty          |
```

```gherkin
Feature 2: View expenses
    In order to review spending
    As a user
    I want to view all stored expenses

    Background:
        Given the application is running

    Scenario: View all expenses when records exist
        Given the following expenses exist:
            | title | amount | category |
            | Lunch | 12.50  | Food     |
            | Rent  | 800.00 | Housing  |
        When I request to view all expenses
        Then I see a list containing 2 expenses
        And each expense shows title, amount and category

    Scenario: View all expenses when none exist
        Given no expenses are stored
        When I request to view all expenses
        Then I see the message "No Expenses Found"
```

```gherkin
Feature 3: Filter expenses by category
    In order to analyse category spending
    As a user
    I want to filter expenses by category

    Background:
        Given the application is running

    Scenario: Filter returns matching category (case-insensitive)
        Given the following expenses exist:
            | title | amount | category |
            | Coffee| 3.50   | Food     |
            | Pizza | 10.00  | food     |
        When I filter expenses by category "food"
        Then I see only expenses in category "Food"

    Scenario: Filter with no matches
        Given stored expenses exist
        When I filter expenses by category "Nonexistent"
        Then I see the message "No expenses found"
```

```gherkin
Feature 4: Delete expenses
    In order to remove mistakes
    As a user
    I want to delete an expense by index

    Background:
        Given the application is running

    Scenario: Delete an expense with valid index
        Given the following expenses exist:
            | title | amount | category |
            | Tea   | 2.50   | Food     |
        When I delete the expense at index 1
        Then the expense is removed from the list
        And the change persists in "data/expenses.json"
        And an INFO log entry is created

    Scenario: Attempt to delete with invalid index
        Given stored expenses exist
        When I delete the expense at index 99
        Then no expense is removed
        And an error message "Invalid index" is shown
        And a WARNING log entry is created
```

```gherkin
Feature 5: Show total spending
    In order to understand total outflow
    As a user
    I want to see the total amount spent

    Background:
        Given the application is running

    Scenario: Calculate total with multiple expenses
        Given the following expenses exist:
            | title | amount | category |
            | A     | 1.00   | Misc     |
            | B     | 2.50   | Misc     |
        When I request the total spending
        Then the displayed total is 3.50

    Scenario: Calculate total when no expenses exist
        Given no expenses are stored
        When I request the total spending
        Then the displayed total is 0.00
```

```gherkin
Feature 6: Data persistence and resilience
    In order to keep user data safe
    As the application
    I must persist data and handle corrupted storage

    Background:
        Given the application is running

    Scenario: Data persists between runs
        Given I add an expense with title "Lunch" and amount 10.00 and category "Food"
        When the application restarts
        Then the expense list contains an expense with title "Lunch"

    Scenario: Handle corrupted JSON store gracefully
        Given data/expenses.json is corrupted
        When the application starts
        Then the application warns "Data file corrupted"
        And the application does not crash
        And the application offers to recover or recreate the data file
```

# Non-functional requirements

- **Logging**: 
  success operations log at INFO; invalid attempts log at WARNING. Logs written to logs/app.log.
- **Storage**: expenses are stored in data/expenses.json and must survive restarts.
- **Error handling**: invalid inputs and corrupted JSON must be handled gracefully; CLI must not crash.
- **Testability**: business logic separated from CLI to allow unit tests.
- **Performance**: should handle ~1000 expenses without noticeable delay.
- **Environment**: Python 3.9+; cross-platform (macOS/Windows/Linux).

``` 
