import uuid
import random
import json
from faker import Faker
from unittest.mock import patch
import requests
from behave import given, when, then

fake = Faker()
API_URL = "https://localhost/api/transactions"


@given("a random transaction is generated")
def step_generate_transaction(context):
    """Generate a valid random transaction."""
    context.transaction = {
        "transaction_id": str(uuid.uuid4()),
        "amount": round(random.uniform(1.00, 5000.00), 2),
        "currency": random.choice(["USD", "EUR", "GBP", "JPY", "CAD"]),
        "timestamp": fake.iso8601(),
        "sender": fake.name(),
        "receiver": fake.name(),
        "status": random.choice(["pending", "completed", "failed"]),
        "description": fake.sentence(),
    }


@when("the transaction is sent to the API")
def step_send_transaction(context):
    """Mock sending the transaction to the API."""
    with patch("requests.post") as mock_post:
        # Mock response with a 200 status code
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({"transaction_id": context.transaction["transaction_id"]}).encode("utf-8")

        # Configure the mock to return the fake response
        mock_post.return_value = mock_response

        # Call the function that would normally send the request
        response = requests.post(API_URL, json=context.transaction)
        context.response = response


@then("the API should return a 200 response")
def step_check_response_status(context):
    """Check if mocked API response is 200 OK."""
    assert context.response is not None, "No response received"
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"


@then("the response should contain the transaction ID")
def step_check_response_content(context):
    """Validate that the mock response contains the correct transaction ID."""
    json_response = context.response.json()
    assert "transaction_id" in json_response, "Transaction ID missing from response"
    assert json_response["transaction_id"] == context.transaction["transaction_id"], "Transaction ID mismatch"


@when("the API is down")
def step_api_down(context):
    """Mock API failure by simulating a 500 response."""
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 500  # Simulating server error
        mock_post.return_value = mock_response

        response = requests.post(API_URL, json=context.transaction)
        context.response = response


@then("the transaction should not be sent successfully")
def step_transaction_not_sent(context):
    """Ensure the transaction fails when the API is down."""
    assert context.response is not None, "No response received"
    assert context.response.status_code != 200, f"Expected failure, but got {context.response.status_code}"

