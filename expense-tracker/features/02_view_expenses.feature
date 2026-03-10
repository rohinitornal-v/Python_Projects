# View Expense

Feature: View all Expenses
  As a user of the Expense Tracker
  I want to view all stored expenses
  So that I can review my spending history

  Background:
    Given the expense tracker application is running
    And the following expenses exist:

      | title          | amount  | category  |
      | Coffee         | 3.50    | Beverages |
      | Gym Membership | 49.99   | Fitness   |
      | Bus Ticket     | 1.25    | Transport |
      | Rent           | 1500.00 | Housing   |
      | Lunch          | 30.00   | FOod      |

  # Happy path

  Scenario: View all expenses sorted by amount descending
    When I request to view all the expenses
    Then each expense should be displayed in descending order of amount
    And the first exepnse should be "Rent" with amount 1500.00
    And the last expense should be "Bus Ticket" with amount 1.25

  Scenario: View expenses displays index number
    When I request to view all Expenses
    Then each expense should be dispalyed with an index number
    And the index should start from 1

  Scenario: View expenses when store is empty
    Given the expense store is empty
    When I request to view all expenses
    Then the system should display an empty list message