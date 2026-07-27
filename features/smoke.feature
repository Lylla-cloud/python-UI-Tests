Feature: Smoke Test website availability

  Scenario: Home page load
    Given I navigate to the Automation Exercise home page
    Then the page title should contain "Automation Exercise"
