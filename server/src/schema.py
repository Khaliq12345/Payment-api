from enum import Enum

from pydantic import BaseModel


class Country(Enum):
    benin = "bj"
    togo = "tg"
    cote_divoire = "ci"
    senegal = "sn"
    niger = "ne"
    mali = "ml"
    burkina_faso = "bf"


class Platform(Enum):
    whatsapp = "whatsapp"
    email = "email"


class Customer(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    whatsapp_phone: str
    country: Country
    product_id: str


class Transaction(BaseModel):
    title: str
    full_name: str
    description: str
    amount: int
    platform: Platform
    customer_id: str
    product_id: str
    email: str
    whatsapp_phone: str
    group_id: str | None = None
    drive_link: str | None = None
    status: str
    created_at: str
    id: int
    reference: str
    approved_at: str
    receipt_url: str


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float = 100.0
    platform: Platform
    drive_link: str | None = None
    whatsapp_groupid: str | None = None
