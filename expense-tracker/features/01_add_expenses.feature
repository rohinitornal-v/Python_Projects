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

  Scenario Outline: Successfully add expenses with various valid inputs
    When I add an expense with title "<title>", amount <amount>, and category "<category>"
    Then the expense should be saved to "data/expenses.json"
    And the expense list should contain an entry with title "<title>", amount <amount>, category "<category>"

    Examples:
      | title          | amount  | category  |
      | Coffee         | 3.50    | Beverages |
      | Gym Membership | 49.99   | Fitness   |
      | Bus Ticket     | 1.25    | Transport |
      | Rent           | 1500.00 | Housing   |
      | Lunch          | 30.00   | Food      |

  # Invalid Validation - Title

  Scenario: Reject expense with empty Title
    When I try to add an expense with title "", amount 10.00, and category "Food"
    Then the application should raise an error "Title cannot be empty"
    And no expense should be saved to "data/expenses.json"
    And the application should not crash

  # Invalid Validation - Amount

  Scenario: Reject expense with zero amount
    When I try to add an expense with title "Coffee", amount 0, and category "Beverages"
    Then the application should raise an error "Amount must be greater than 0"
    And no expense should be saved to "data/expenses.json"
    And the application should not crash

  Scenario: Reject expense with negative amount
    When I try to add an expense with title "Coffee", amount -3.00, and category "Beverages"
    Then the application should raise an error "Amount must be greater than 0"
    And no expense should be saved to "data/expenses.json"
    And the application should not crash

  Scenario: Reject expense with alpha numeric amount
    When I try to add an expense with title "Coffee", amount "hg5.00", and category "Beverages"
    Then the application should raise an error "Amount must be numeric"
    And no expense should be saved to "data/expenses.json"
    And the application should not crash

  #Invalid validation - Category

  Scenario: Reject expense with empty Category
    When I try to add an expense with title "Coffee", amount 3.50, and category ""
    Then the application should raise an error "Category cannot be empty"
    And no expense should be saved to "data/expenses.json"
    And the application should not crash

  # Data Persistence

  Scenario: Expense data persist after the application restarts
    Given I have added an expense with title "Dinner", amount 3.50, and category "Food"
    When the application is restarted
    Then the expense list should still contain an entry with title "Dinner", amount 3.50, category "Food"
