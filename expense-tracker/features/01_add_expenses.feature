# Gherkin

Feature: Add Expense
  As a user of the Expense Tracker
  I want to add expenses with a title, amount, and category
  So that I can track my spending

  Background:
    Given the expense tracker application is running
    And the expense store is empty

  # Happy Path

  Scenario: Successfully add a valid expense
    When I add an expense with title "Lunch", amount 12.50, and category "Food"
    Then the expense should be saved to "data/expenses.json"
    And the expense list should contain an entry with title "Lunch", amount 12.50, category "Food"
    And an INFO log entry "Added Expenses: Lunch" should be written to "logs/app.log"

