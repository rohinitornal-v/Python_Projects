# Total spendings

Feature: Show Total Spending
  As a user of the Expense Tracker
  I want to see the total amount spent
  So that I can understand my overall spendings

  Background:
    Given the expense tracker is running

  # Happy Path

  Scenario:  Calculate Total with multiple expenses
    Given the following expenses exist:

      | title          | amount  | category  |
      | Coffee         | 3.50    | Beverages |
      | Gym Membership | 49.99   | Fitness   |
      | Bus Ticket     | 1.25    | Transport |
      | Rent           | 1500.00 | Housing   |
      | Lunch          | 30.00   | Food      |
      | Tea            | 1.50    | Beverages |
    When the user selects "Show Total"
    Then the system should calculate the sum of all expenses
    And display the correct numeric total 1586.24

  Scenario:  Calculate Total with single expenses
    Given the following expenses exist:

      | title  | amount | category  |
      | Coffee | 3.50   | Beverages |

    When the user selects "Show Total"
    Then the system should calculate the sum of all expenses
    And display the correct numeric total 3.50

  # Empty Store

  Scenario: Calculate Total with no expenses
    Given the expense store is empty
    When the user selects "Show Total"
    Then the system should return a total 0.00

  # Data Integrity

  Scenario: Total result is always numeric
    Given at least one expense exist
      | title  | amount | category  |
      | Coffee | 3.50   | Beverages |
    When the user selects "Show Total"
    Then the result should be a numeric value
