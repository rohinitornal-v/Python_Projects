# Expense Tracker CLI
## BDD requirements document
Author: Rohini
Version: 1.0

----
# Feature 1 : Add Expense
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
When the user enters a non-numeric or negative amount
Then the system should display an error
And the expense should not be saved