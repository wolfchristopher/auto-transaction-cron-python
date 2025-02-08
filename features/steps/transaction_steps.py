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
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({"transaction_id": context.transaction["transaction_id"]}).encode("utf-8")

        mock_post.return_value = mock_response

        response = requests.post(API_URL, json=context.transaction)
        context.response = response


@then("the API should return a 200 response")
def step_check_response_status(context):
    assert context.response is not None, "No response received"
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"


@then("the response should contain the transaction ID")
def step_check_response_content(context):
    json_response = context.response.json()
    assert "transaction_id" in json_response, "Transaction ID missing from response"
    assert json_response["transaction_id"] == context.transaction["transaction_id"], "Transaction ID mismatch"


@when("the API is down")
def step_api_down(context):
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        response = requests.post(API_URL, json=context.transaction)
        context.response = response


@then("the transaction should not be sent successfully")
def step_transaction_not_sent(context):
    assert context.response is not None, "No response received"
    assert context.response.status_code != 200, f"Expected failure, but got {context.response.status_code}"



API_URL_1 = "https://example.com/api/processed_transactions"  # Mock API

def send_transformed_transaction(transaction):

    if not transaction or "amount" not in transaction:
        print("Invalid transaction data:", transaction)
        return None

    new_amount = round(random.uniform(1.00, 1000.00), 2)
    updated_amount = transaction["amount"] + new_amount

    processed_transaction = {
        **transaction,
        "new_amount": new_amount,
        "tax": round(updated_amount * 0.05, 2),
        "discount": round(updated_amount * 0.10, 2),
        "final_amount": round(updated_amount + (updated_amount * 0.05) - (updated_amount * 0.10), 2)
    }

    try:
        response = requests.post(API_URL_1, json=processed_transaction)
        return response
    except requests.RequestException as e:
        print(f"Error sending transaction: {e}")
        return None

@given("a valid transaction is available")
def step_valid_transaction(context):
    context.transaction = {
        "transaction_id": "abc123",
        "amount": 100.00,
        "currency": "USD",
        "sender": "Alice",
        "receiver": "Bob"
    }

@given("an invalid transaction without an amount")
def step_invalid_transaction(context):
    context.transaction = {
        "transaction_id": "xyz789",
        "currency": "USD",
        "sender": "Alice",
        "receiver": "Bob"
    }

@when("the transaction is transformed and sent to the API")
def step_send_transaction(context):
    with patch("requests.post") as mock_post:
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps({
            "message": "Transaction processed",
            "transaction_id": context.transaction.get("transaction_id"),
            "new_amount": 50.00,
            "tax": 7.50,
            "discount": 15.00,
            "final_amount": 92.50
        }).encode("utf-8")
        mock_post.return_value = mock_response

        context.response = send_transformed_transaction(context.transaction)

@then("the API 1 should return a 200 response")
def step_check_response_status(context):
    assert context.response is not None, "No response received"
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}"

@then("the processed transaction should include new calculated fields")
def step_check_processed_fields(context):
    json_response = context.response.json()
    assert "new_amount" in json_response, "Missing new_amount"
    assert "tax" in json_response, "Missing tax"
    assert "discount" in json_response, "Missing discount"
    assert "final_amount" in json_response, "Missing final_amount"

@then("the process should fail gracefully")
def step_check_failure(context):
    response = send_transformed_transaction(context.transaction)
    assert response is None, "Expected None for invalid transaction"

