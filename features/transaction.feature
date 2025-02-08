Feature: Transaction Generator API

  Scenario: Send a valid transaction
    Given a random transaction is generated
    When the transaction is sent to the API
    Then the API should return a 200 response
    And the response should contain the transaction ID

  Scenario: Handle API failure
    Given a random transaction is generated
    When the API is down
    Then the transaction should not be sent successfully


  Scenario: Successfully send a transformed transaction
    Given a valid transaction is available
    When the transaction is transformed and sent to the API
    Then the API 1 should return a 200 response
    And the processed transaction should include new calculated fields

  Scenario: Handle missing amount field in transaction
    Given an invalid transaction without an amount
    When the transaction is transformed and sent to the API
    Then the process should fail gracefully