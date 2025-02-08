import requests
import random
import time
import uuid
import schedule
from faker import Faker

fake = Faker()

API_URL = "https://example.com/api/transactions"  # Replace with the actual API endpoint

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
    try:
        response = requests.post(API_URL, json=transaction)
        print(f"Sent Transaction: {transaction}")
        print(f"Response: {response.status_code}, {response.text}")
    except requests.RequestException as e:
        print(f"Error sending transaction: {e}")

# Schedule the job to run every second
schedule.every(1).seconds.do(send_transaction)

# Run the scheduler
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)