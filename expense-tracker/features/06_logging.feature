# Log for Expense Tracker

Feature: Application Logging
  As a developer
  I want all key operations to be logged
  So that I can audit and debug the application

  Background:
    Given the expense tracker application is running
    And the log file "logs/app.log" exists

  # INFO Logging

  Scenario: Log INFO for adding an expense
    When I add an expense with title "Dinner", amount 25.00, and category "Food"
    Then an INFO log entry "Added expense: Dinner, Amount: 25.0, Category: Food" should be written to "logs/app.log"

  Scenario: Log INFO for deleting an expense
    Given the following expenses exist:

      | title  | amount | category  |
      | Coffee | 3.50   | Beverages |

    When I delete the expense at index 1
    Then an INFO log entry "Deleted expense at index: 1" should be written to "logs/app.log"

  # WARNING Logging

  Scenario: WARNING log message for out-of-range delete index
    Given the following expenses exist:
      | title  | amount | category |
      | Coffee | 4.50   | Food     |
    When I try to delete the expense at index 5
    Then a WARNING log entry "Invalid delete index: 5" should be written to "logs/app.log"

  Scenario: WARNING log message for negative delete index
    Given the following expenses exist:
      | title  | amount | category |
      | Coffee | 4.50   | Food     |
    When I try to delete the expense at index -2
    Then a WARNING log entry "Invalid delete index: -2" should be written to "logs/app.log"

  # Log File Creation

  Scenario: Log file is created automatically on first run
    Given the log file does not exist
    When the expense tracker application is started and performs any operation that requires logging
    Then the log file "logs/app.log" should be created automatically
