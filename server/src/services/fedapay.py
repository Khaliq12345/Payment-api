import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class FedaPay:
    def __init__(self) -> None:
        self.url = "https://api.fedapay.com/v1"
        self.token = os.getenv("FEDAPAY_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def create_customer(self, customer_data: dict) -> dict:
        payload = {
            "email": customer_data["email"],
            "phone_number": {
                "number": customer_data["phone_number"],
                "country": customer_data["country"],
            },
            "firstname": customer_data["first_name"],
            "lastname": customer_data["last_name"],
        }

        response = httpx.post(
            f"{self.url}/customers", json=payload, headers=self.headers
        )
        return response.json()

    def create_transaction(self, transaction_data: dict) -> dict:
        payload = {
            "description": transaction_data["description"],
            "amount": transaction_data["amount"],
            "currency": {"iso": transaction_data["currency"]},
            "callback_url": transaction_data["callback_url"],
            "custom_metadata": {
                "whatsapp_number": transaction_data["whatsapp_number"],
                "group_id": transaction_data["group_id"],
            },
            "customer": {
                "id": transaction_data["customer_id"],
            },
        }

        response = httpx.post(
            f"{self.url}/transactions", json=payload, headers=self.headers
        )
        return response.json()

    def get_transaction(self, transactionId: str) -> dict:
        url = f"{self.url}/transactions/{transactionId}"
        response = httpx.get(url, headers=self.headers)
        return response.json()
