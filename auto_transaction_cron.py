import requests
import random
import time
import uuid
import schedule
from faker import Faker

fake = Faker()

API_URL_1 = "http://127.0.0.1:4000/dataset1"  # Replace with the actual API endpoint 1
API_URL_2 = "http://127.0.0.1:4000/dataset2" # Replace with the actual API endpoint 2

def generate_transaction():
    return {
        "transaction_id": str(uuid.uuid4()),
        "amount": round(random.uniform(1.00, 5000.00), 2),
        "currency": random.choice(["USD", "EUR", "GBP", "JPY", "CAD"]),
        "timestamp": fake.iso8601(),
        "sender": fake.name(),
        "receiver": fake.name(),
        "status": random.choice(["pending", "completed", "failed"]),
        "description": fake.sentence(),
    }

def send_transaction():
    transaction = generate_transaction()
    send_transformed_transaction(transaction)
    try:
        response = requests.post(API_URL_1, json=transaction)
        print(f"Sent Transaction: {transaction}")
        print(f"Response: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Error sending transaction: {e}")

schedule.every(1).seconds.do(send_transaction)

def send_transformed_transaction(transaction):
    if not transaction or "amount" not in transaction:
        print("Invalid transaction data:", transaction)
        return None

    # Generate a new random amount
    new_amount = round(random.uniform(1.00, 1000.00), 2)
    updated_amount = transaction["amount"] + new_amount

    processed_transaction = {
        **transaction,
        "new_amount": new_amount,
        "tax": round(updated_amount * 0.05, 2),
        "discount": round(updated_amount * 0.10, 2),
        "final_amount": round(updated_amount + (updated_amount * 0.05) - (updated_amount * 0.10), 2)
    }

    # Decide whether to change the amount for dataset 2 (only 10% of the time)
    if random.random() < 0.10:  # 10% chance
        altered_amount = round(random.uniform(1.00, 1000.00), 2)
    else:
        altered_amount = transaction["amount"]

    dataset2_transaction = {
        **processed_transaction,
        "amount": altered_amount  # Use altered amount only 10% of the time
    }

    try:
        # Send to dataset 1 (regular processed transaction)
        response_1 = requests.post(API_URL_1, json=processed_transaction)
        print(f"Sent Transaction to Dataset 1: {processed_transaction}")
        print(f"Response: {response_1.status_code}, {response_1.text}")

        # Send to dataset 2 with potential altered amount
        response_2 = requests.post(API_URL_2, json=dataset2_transaction)
        print(f"Sent Transaction to Dataset 2: {dataset2_transaction}")
        print(f"Response: {response_2.status_code}, {response_2.text}")

    except requests.RequestException as e:
        print(f"Error sending transaction: {e}")


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)