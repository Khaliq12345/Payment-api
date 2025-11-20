from enum import Enum

from pydantic import BaseModel


class Country(Enum):
    benin = "bj"


class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    country: Country


class Transaction(BaseModel):
    description: str
    amount: int
    currency: str
    callback_url: str
    customer_id: int
    whatsapp_number: int
    group_id: int
