# Data Persistence

Feature: Data Persistence
  As a user of the Expense Tracker
  I want my expenses to be saved between sessions
  So that my data is not lost when the application closes

  Background:
    Given the expense tracker application is running
    And the expense data file "data/expenses.json" exists

  # Happy Path

  Scenario: Expenses persist after application restart

    Given I add a new expense with title "Lunch", amount 25.00, and category "Food"
    When the application is restarted
    Then the expense "Lunch" with amount 25.00 and category "Food" should still exist in the list of expenses
    And the amount should still be 25.00
    And the category should still be "Food"

  Scenario: Multiple expenses persist after application restart
    Given the following expenses exist:

      | title  | amount | category  |
      | Coffee | 3.50   | Beverages |
      | Lunch  | 25.00  | Food      |

    When the application is restarted
    Then the all 2 expenses should still exist in the list of expenses

  Scenario: Deleted expenses do not persist after restart
    Given the following expenses exist:

      | title  | amount | category  |
      | Coffee | 3.50   | Beverages |
      | Lunch  | 25.00  | Food      |

    When I delete the expense at index 1
    And the application is restarted
    Then only 1 expense shouldl exist in the list of expenses

  # Error Handling

  Scenario: Application handles corrupted JSON file gracefully
    Given the file "data/expenses.json" contains invalid JSON
    When I start the application
    Then the application should not crash
    And the system should display an appropriate error message