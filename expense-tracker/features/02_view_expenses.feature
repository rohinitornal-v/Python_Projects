# View Expense

Feature: View all Expenses
  As a user of the Expense Tracker
  I want to view all stored expenses
  So that I can review my spending history

  Background:
    Given the expense tracker application is running
    And the following expenses exist:
      | title     | amount | category  |
      | Groceries | 50.00  | Food      |
      | Bus Pass  | 30.00  | Transport |
      | Netflix   | 15.00  | Subsidary |

  # Happy path

  Scenario: View all expenses sorted by amount descending
    When I request to view all the expenses
    Then each expense should be displayed in descending order of amount
    And the first exepnse should be "Groceries" with amount 50.00
    And the last expense should be "Netflix" with amount 15.00

  Scenario: View expenses displays index number
    When I request to view all Expenses
    Then each expense should be dispalyed with an index number
    And the index should start from 1

  Scenario: View expenses when store is empty
    Given the expense store is empty
    When I request to view all expenses
    Then the system should display an empty list message