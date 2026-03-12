# Performance Feature

Feature: Performance
  As a user of the Expense Tracker
  I want the application to handle large data sets efficiently
  So that performance does not degrade with more expenses

  Background:
    Given the expense tracker application is running
    And the expense store is empty

  # Happy Path

  Scenario: Application handles 1000 expenses without noticable delay
    Given I add 1000 expenses to the store
    When I request to view all the expenses
    Then the response time should be under 2 seconds

  Scenario: Filter performs within acceptable time with 1000 expenses
    Given I add 1000 expenses to the store
    When I filter expenses by category "Food"
    Then the response time should be under 2 seconds

  Scenario: Total calculation performs within acceptable time with 1000 expenses
    Given I add 1000 expenses to the store
    When I select "Show Total"
    Then the response time should be under 2 seconds

  Scenario: Delete performs within acceptable time with 1000 expenses
    Given I add 1000 expenses to the store
    When I delete the expense at index 500
    Then the response time should be under 2 seconds