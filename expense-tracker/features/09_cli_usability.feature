# CLI usability Feature

Feature: CLI Usability
  As a user of the Expense Tracker CLI
  I want the command-line interface to be intuitive and user-friendly
  So that I can easily manage and view my expenses without confusion

  Background:
    Given the expense tracker application is running
    And the expense store is empty

  # Happy Path

  Scenario: Display main menu on startup
    When I start the application
    Then the CLI should display the following options:
      | Option                         |
      | 1. Add Expense                 |
      | 2. View All Expenses           |
      | 3. Filter Expenses by Category |
      | 4. Delete Expense              |
      | 5. Show Total Spending         |
      | 6. Exit                        |

  Scenario: Handle invalid menu option gracefully
    Given the main menu is displayed
    When I enter an invalid option "9xyz"
    Then the application should display "Invalid option, please try again."
    And the main menu should be displayed again
    And the application should not crash

  Scenario: Handle empty menu gracefully
    Given the main menu is displayed
    When I enter an empty menu option
    Then the application should display "Invalid option, please try again."
    And the main menu should be displayed again
    And the application should not crash

  # Exit

  Scenario: Exit the application cleanly
    Given the main menu is displayed
    When I select menu option "6"
    Then the application should display "Goodbye!"
    And the application should terminate without errors
