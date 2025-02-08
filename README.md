# auto-transaction-cron-python
This is a cron job that generates random transactions and sends them to an api endpoint.

## Overview
This application consists of two cron jobs that handle transaction generation and processing. The system:
- Generates random transactions and sends them to an API.
- Transforms transactions by adding new fields and updates the amount before sending them to another API.
- Includes a Flask API to receive transactions.
- Supports BDD testing with Behave and mocks API calls.

## Features
✅ Generates random transactions every second  
✅ Processes transactions by adding new fields (`new_amount`, `tax`, `discount`, `final_amount`)  
✅ Sends transactions to a secondary API endpoint
✅ Supports BDD testing with Behave  
✅ Uses `schedule` for cron job-like execution  

## Project Structure
```
transaction_cron/
├── transaction_generator.py                # Generates transactions and sends to API 
├── transaction_processor.py                # Processes transactions and sends them to another API
├── transaction_receiver.py                 # Flask API to receive transactions
├── features/                               # BDD test files
│   ├── transaction_processing.feature
│   ├── steps/
│       ├── transaction_processing_steps.py
├── requirements.txt                        # Dependencies
├── README.md                               # Documentation
```
## Installation
### Clone the Repository

To get started, clone the repository using the following command:

```sh
git clone https://github.com/wolfchristopher/auto-transaction-cron-python.git
cd auto-transaction-cron-python
```

### Create and Activate a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```
### Install Dependencies
```sh
pip install -r requirements.txt
```
## Running the App
### Start Application
```sh
python auto_transaction_cron.py
```
## Running BDD Tests
### Run Tests
```shell
behave
```

## License
This project is licensed under the MIT License.
## Contributors
- Christopher Wolf