# Expense Tracker CLI
## BDD requirements document
Author: Rohini
Version: 1.0

----
# Feature 1 : Add Expenses
As a user
I want to add a new expense
So that I can track my spending

## Scenario: Add valid expense
Given the application is running
When the user enters a valid title, amount, and category
Then the expense should be saved
And the expense should persist in expense.json
And a log entry should be created

## Scenario: Add expense with empty title
Given the application is running
When the user enters an empty title
Then the system should display an error
And the expense should not be saved

## Scenario: Add expense with invalid amount
Given the application is running
When the user enters a non-numeric or negative amount or 0 amount
Then the system should display an error
And the expense should not be saved

## Scenario: Add expense with empty category
Given the application is running
When the user enters an empty category
Then the system should display an error
And the expense should not be saved

# Feature 2 : View All Expenses
As a user
I want to view all expenses
So that I can review my spending

## Scenario: View expenses when record exist
Given there are stored expenses
When the user selects "View All"
Then all expenses should be displayed
And they should be sorted by amount decending

## Scenario: View expenses when empty
Given there are no stored expenses
When the user selects "View All"
Then the system should display "No Expenses Found"

# Feature 3 : Filter By Category
As a User
I want to filter expenses by category
So that I can see category-based spending

## Scenario: Filter with matching category
Given stored expenses exist
When the user enters a valid category
Then matching expenses should be displayed

## Scenario: Filter with no matching category
Given stored expenses exist
When the user enters a category with no matches
Then the system should display "No expenses found"

# Feature 4 : Delete expenses
As a User
I want to delete an expense
So that I can correct mistakes

## Scenario: Delete valid expense
Given stored expenses exist
When the user enters valid index
Then the expense should be deleted
And the change should persist in expenses.json
And a log enrty should be created

## Scenario: Delete invalid Index
Given stored expenses exist
When the user enters an invalid index
Then the system should display an error
And no expense should be deleted
And a warning log should be created

# Feature 5 : Show Total Spending
As a User
I want to see the total amount spent
So that I can understand overall spending

## Scenario: Calculate Total
Given stored expenses exist
When the user selects "Show Total"
Then the system calculate the sum of all expenses
And display the correct numeric total

# Non-Functional Requirements

## Logging
    - All successfull add and delete operations must log at INFO level
    - Invalid operations must log at WARNING level
    - Logs must be written to log/app.log

## Data Persistance
    - Data must be stored in data/expenses.json
    - Data must persist between runs

## Error handling
    - Application must not crash on invalid user input
    - JSON corruption must be handled gracefully

## Testability
    - Bussiness logic must be unit testable
    - CLI logic must be seperate from core logic