# Filter Expenses

Feature: Filter Expenses by Category
  As a User of the Expense Tracker
  I want to filter expenses by category
  So that I can see category-based spending

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

  Scenario: Filter expenses with an exact matching category
    When I filter expenses by category "Food"
    Then only expenses in category "Food" should be displayed
    And the result should contain "Lunch"
    And other categories should not be in the result

  Scenario: Filter expenses with case-insensitive category match
    When I filter expenses by category "food"
    Then only expenses in category "Food" should be displayed
    And the result should contain "Lunch"

  Scenario: Filter result are stored by amount descending
    When I filter expenses by category "Beverages"
    Then the results should be displayed in descending order of amount
    And the first result should be "Coffee" with amount 3.50

  # Empty and no match

  Scenario: Filter expenses with no matching category
    When I filter expenses by category "Entertainment"
    Then the application should display a message "No Expense Found"

  # Input Validation

  Scenario: Filter expenses with empty category input
    When I filter expenses by category ""
    Then the application should raise an error "Category cannot be empty"
    And the application should not crash
