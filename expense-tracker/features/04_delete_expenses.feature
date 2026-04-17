# Delete Expenses

Feature: Delete Expenses
  As a user of the Expense Tracker
  I want to delete an expense by its index
  So that I can correct mistakes

  Background:
    Given the expense tracker application is running
    And the following expenses exist:

      | title          | amount  | category  |
      | Coffee         | 3.50    | Beverages |
      | Gym Membership | 49.99   | Fitness   |
      | Bus Ticket     | 1.25    | Transport |
      | Rent           | 1500.00 | Housing   |
      | Lunch          | 30.00   | Food      |
      | Tea            | 1.50    | Beverages |

  # Happy Path

  Scenario: Successfully delete a valid expense
    When I delete the expense at index 2
    Then the expense "Gym Membership" should be removed from the list
    And the change should be saved to "data/expenses.json"
    And an INFO log entry "Deleted expense at index: 2" should be written to "logs/app.log"

  # Input Validation

  Scenario: Reject delete with an out-of-range index
    When I delete the expense at index 10
    Then the application should raise an error "Invalid Index"
    And no expense should be deleted
    And a WARNING log entry "Invalid delete index: 10" should be written to "logs/app.log"

  Scenario: Reject delete with a negative index
    When I delete the expense at index -3
    Then the application should raise an error "Invalid Index"
    And no expense should be deleted
    And a WARNING log entry "Invalid delete index: -3" should be written to "logs/app.log"

  Scenario: Reject delete with a Zero index
    When I delete the expense at index 0
    Then the application should raise an error "Invalid Index"
    And no expense should be deleted
    And a WARNING log entry "Invalid delete index: 0" should be written to "logs/app.log"

  # Empty Store

  Scenario: Reject delete when expense store is empty
    Given the expense store is empty
    When I try to delete the expense at index 1
    Then the application should raise a validation error "No expenses found"
    And a WARNING log entry should be written to "logs/app.log"
