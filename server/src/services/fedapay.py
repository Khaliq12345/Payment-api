import os
from typing import Any

import httpx
from dotenv import load_dotenv

from src.schema import Customer as CustomerSchema
from src.schema import Transaction
from src.storage.database import Database

load_dotenv()


class FedaPay:
    def __init__(self) -> None:
        self.url = "https://api.fedapay.com/v1"
        self.token = os.getenv("FEDAPAY_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        self.database = Database()

    def create_customer(self, customer_data: CustomerSchema) -> dict:
        """Create a new customer"""
        payload = {
            "email": customer_data.email,
            "phone_number": {
                "number": customer_data.phone,
                "country": customer_data.country.value,
            },
            "firstname": customer_data.first_name,
            "lastname": customer_data.last_name,
        }

        response = httpx.post(
            f"{self.url}/customers", json=payload, headers=self.headers
        )
        if response.status_code == 400:
            # """Search for customer in Fedapay"""
            response = self.search_customer(customer_data.email)
            if not response:
                raise ValueError("Customer not in Fedapay")
            return response
        response.raise_for_status()
        json_data = response.json()
        return json_data["v1/customer"]

    def retrieve_customer(self, customer_id: str) -> dict:
        """Retrieve a customer info with the customer id"""
        response = httpx.get(
            f"{self.url}/customers/{customer_id}", headers=self.headers
        )
        json_data = response.json()
        return json_data["v1/customer"]

    def search_customer(self, email: str) -> dict | None:
        """Find a customer by email"""
        response = httpx.get(f"{self.url}/customers/search", headers=self.headers)
        response.raise_for_status()
        json_data = response.json()
        for customer in json_data["v1/customers"]:
            if not customer["email"] == email:
                continue
            return customer

    def create_transaction(
        self, product_id: str, customer_id: str, callback_url: str
    ) -> dict | None:
        """Create transaction from the product and customer"""
        customer = self.database.retrieve_customer(
            customer_id=customer_id, product_id=product_id
        )
        if not customer:
            return None
        product = self.database.get_product(product_id=product_id)
        if not product:
            return None
        payload = {
            "description": product.description,
            "amount": product.price,
            "currency": {"iso": "XOF"},
            "callback_url": callback_url,
            "custom_metadata": {
                "title": product.title,
                "platform": product.platform,
                "email": customer.email,
                "whatsapp_phone": customer.whatsapp_phone,
                "group_id": product.whatsapp_groupid,
                "drive_link": product.drive_link,
                "customer_id": customer.id,
                "product_id": product.id,
            },
            "customer": {
                "id": customer.fedapay_id,
            },
        }

        response = httpx.post(
            f"{self.url}/transactions", json=payload, headers=self.headers
        )
        response.raise_for_status()
        json_data = response.json()
        return json_data["v1/transaction"]["payment_url"]

    def get_transaction(self, transactionId: Any) -> Transaction:
        url = f"{self.url}/transactions/{transactionId}"
        response = httpx.get(url, headers=self.headers)
        response.raise_for_status()
        json_data = response.json()
        transaction = json_data["v1/transaction"]
        metadata = transaction["custom_metadata"]
        first_name = transaction["metadata"]["paid_customer"]["firstname"]
        last_name = transaction["metadata"]["paid_customer"]["lastname"]
        return Transaction(
            status=transaction["status"],
            created_at=transaction["created_at"],
            id=transaction["id"],
            reference=transaction["reference"],
            approved_at=transaction["approved_at"],
            receipt_url=transaction["receipt_url"],
            description=transaction["description"],
            amount=transaction["amount"],
            customer_id=metadata["customer_id"],
            product_id=metadata["product_id"],
            title=metadata["title"],
            full_name=f"{first_name} {last_name}",
            platform=metadata["platform"],
            email=metadata["email"],
            whatsapp_phone=metadata["whatsapp_phone"],
            group_id=metadata["group_id"],
            drive_link=metadata["drive_link"],
        )
