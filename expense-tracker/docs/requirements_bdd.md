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
And the application should not crash

## Scenario: Add expense with zero amount
Given the application is running
When the user enters amount as 0
Then the system should display an error "Amount must be greater than 0"
And the expense should not be saved
And the application should not crash

## Scenario: Add expense with negative amount
Given the application is running
When the user enter negative amount
Then the system should display an error "Enter amount greater than 0"
And the expense should not be saved
And the application should not crash

##Scenario: Add expense with non-numeric amount
Given the application is running
When the user enters non-numeric amount
Then the system should display an error "Amount must be numeric"
And the expense should not be saved
And the application should not crash

## Scenario: Add expense with empty category
Given the application is running
When the user enters an empty category
Then the system should display an error
And the expense should not be saved
And the application should not crash

## Scenario Outline: Successfully add expenses with various valid inputs
Given the applicaiton is running
When the useer enters title "<title>", amount "<amount>", and category "<category>"
Then the expense should be saved to "data/expenses.json"

Examples:
  | title          | amount  | category  |
  | Coffee         | 3.50    | Beverages |
  | Gym Membership | 49.99   | Fitness   |
  | Bus Ticket     | 1.25    | Transport |
  | Rent           | 1500.00 | Housing   |
  | Lunch          | 30.00   | FOod      |

## Scenario: Expense data persists after application restart
Given I have added an expense with title "Lunch", amount 30.00, and category "Food"
When the applicaiton restarted
Then the expense list should contain "Lunch"

# Feature 2 : View All Expenses
As a user
I want to view all expenses
So that I can review my spending

## Scenario: View expenses when record exist
Given there are stored expenses
When the user selects "View All"
Then all expenses should be displayed
And they should be sorted by amount decending
And each expense shoiuld be displayed with an index number starting from 1

## Scenario: View expenses when empty
Given there are no stored expenses
When the user selects "View All"
Then the system should display "No Expenses Found"

# Feature 3 : Filter Expenses By Category
As a User
I want to filter expenses by category
So that I can see category-based spending

## Scenario: Filter Expenses with an exact matching category
Given stored expenses exist
When the user filters by category "Food"
Then only "Food" expenses should be displayed

## Scenario: Filter Expenses with case-insensitive category match
Given stored expenses exist
When the user filters by category "food"
Then only "Food" expenses should be displayed

## Scenario: Filter Expenses with no matching category
Given stored expenses exist
When the user filters by category with no matches
Then the system should display "No expenses found"

## Scenario: Filter Expenses with empty category input
Given stored expenses exist
When the user filters by empty category
Then the system should display an error "Category cannot be empty"

## Scenario: Filter results are stored by amount decending
Given stored expenses exist
When the user filters by category "Food"
Then the results should be displayed in decensing order of amount

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
When the user enters an invalid index (out of range index) or negative index
Then the system should display an error
And no expense should be deleted
And a warning log should be created

## Scenario: Delete when expense store is empty
Given the expense store is empty
When the user attempts to delete at index 1
Then the system should display an error
And a warning log should be created

# Feature 5 : Show Total Spending
As a User
I want to see the total amount spent
So that I can understand overall spending

## Scenario: Calculate Total with multiple expenses
Given stored expenses exist
When the user selects "Show Total"
Then the system should calculate the sum of all expenses
And display the correct numeric total

## Scenario: Calculate Total with no expenses
Given the expense store is empty
When the user selects "Show Total"
Then the system should return a total 0.00

## Scenario: Total result is always numeric
Given at least one expense exist
When the user selects "Show Total"
Then the result should be a numeric value

# Non-Functional Requirements

## Logging
    - All successfull add and delete operations must log at INFO level
    - Invalid operations must log at WARNING level
    - Logs must be written to log/app.log

## Data Persistance
    - Data must be stored in data/expenses.json
    - Data must persist between application runs
    - Application must handle corrupted JSON gracefully

## Error handling
    - Application must not crash on invalid user input
    - JSON corruption must be handled gracefully
    - All exceptions must be caught and communicated clearly to the user

## Testability
    - Bussiness logic must be unit testable
    - CLI logic must be seperate from core logic
    - Validation must be reusable across all features

## Performance
    - Application should handle at least 1000 expenses without noticeable delay
  
## System Requirements
    - Python 3.9+
    - No external libraries required
    - Works on macOS/Windows/Linux