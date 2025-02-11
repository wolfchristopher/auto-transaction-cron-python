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
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "amount": float(round(random.uniform(1.00, 5000.00), 2)),
        "currency": random.choice(["USD", "EUR", "GBP", "JPY", "CAD"]),
        "timestamp": fake.iso8601(),
        "status": random.choice(["pending", "completed", "failed"]),
        "description": fake.sentence(),

        # Sender Details
        "sender": {
            "name": fake.name(),
            "account_number": fake.iban(),
            "bank": fake.company(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.email()
        },

        # Receiver Details
        "receiver": {
            "name": fake.name(),
            "account_number": fake.iban(),
            "bank": fake.company(),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.email()
        },

        # Payment Method
        "payment_method": {
            "type": random.choice(["credit_card", "debit_card", "bank_transfer", "paypal", "crypto"]),
            "details": {
                "card_number": fake.credit_card_number() if random.choice([True, False]) else None,
                "expiry_date": fake.credit_card_expire() if random.choice([True, False]) else None,
                "cvv": fake.credit_card_security_code() if random.choice([True, False]) else None,
                "wallet_address": str(fake.uuid4()) if random.choice([True, False]) else None
            }
        },

        # Fees and Charges
        "fees": {
            "service_fee": float(round(random.uniform(0.50, 10.00), 2)),
            "tax": float(round(random.uniform(0.01, 5.00), 2)),
            "discount": float(round(random.uniform(0.00, 20.00), 2)),
            "total": 0  # Placeholder
        },

        # Metadata
        "metadata": {
            "ip_address": fake.ipv4(),
            "device_id": str(fake.uuid4()),
            "user_agent": fake.user_agent(),
            "location": {
                "latitude": float(fake.latitude()),
                "longitude": float(fake.longitude())
            },
            "browser": fake.chrome()
        },

        # Additional Fields
        "is_recurring": random.choice([True, False]),
        "recurring_frequency": random.choice(["daily", "weekly", "monthly", "yearly", None]),
        "invoice_id": str(fake.uuid4()),
        "order_id": str(fake.uuid4()),
        "category": random.choice(["shopping", "subscription", "bill_payment", "donation", "investment"]),
        "loyalty_points_earned": random.randint(0, 100),
        "refund_status": random.choice(["not_requested", "requested", "approved", "declined"]),
        "refund_amount": float(round(random.uniform(0, 5000), 2)),
        "fraud_risk": random.choice(["low", "medium", "high"]),
        "transaction_notes": fake.paragraph(),
        "exchange_rate": float(round(random.uniform(0.5, 1.5), 4)),
        "original_currency": random.choice(["USD", "EUR", "GBP", "JPY", "CAD"]),
        "original_amount": float(round(random.uniform(1.00, 5000.00), 2)),
        "processed_by": fake.name(),
        "transaction_type": random.choice(["purchase", "withdrawal", "transfer", "refund"]),
        "verification_status": random.choice(["verified", "unverified"]),
        "priority": random.choice(["normal", "high", "urgent"]),
        "remarks": fake.sentence(nb_words=10)  # Shortened
    }

    # Fix total calculation (JSON serializable)
    transaction["fees"]["total"] = float(round(
        transaction["fees"]["service_fee"] + transaction["fees"]["tax"] - transaction["fees"]["discount"], 2
    ))

    return transaction

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
        "final_amount": round(updated_amount + (updated_amount * 0.05) - (updated_amount * 0.10), 2),
        "adjusted_status": random.choice(["processed", "review", "declined"]),
        "adjusted_priority": random.choice(["normal", "high", "critical"])
    }

    if random.random() < 0.10:
        altered_amount = round(random.uniform(1.00, 1000.00), 2)
    else:
        altered_amount = transaction["amount"]

    dataset2_transaction = {
        **processed_transaction,
        "amount": altered_amount
    }

    try:
        response_1 = requests.post(API_URL_1, json=processed_transaction)
        print(f"Sent Transaction to Dataset 1: {processed_transaction}")
        print(f"Response: {response_1.status_code}, {response_1.text}")

        response_2 = requests.post(API_URL_2, json=dataset2_transaction)
        print(f"Sent Transaction to Dataset 2: {dataset2_transaction}")
        print(f"Response: {response_2.status_code}, {response_2.text}")
    except requests.RequestException as e:
        print(f"Error sending transaction: {e}")


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


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)