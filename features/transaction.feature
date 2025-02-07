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
