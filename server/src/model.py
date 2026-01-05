from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    # Id généré manuellement
    id: str = Field(primary_key=True)
    title: str
    description: str
    price: float
    platform: str
    drive_link: Optional[str]
    whatsapp_groupid: Optional[str]
    created_at: datetime


class Customer(SQLModel, table=True):
    id: str = Field(primary_key=True)
    first_name: str
    last_name: str
    email: str
    phone: str
    whatsapp_phone: str
    country: str
    created_at: datetime = datetime.now()
    product_id: str = Field(foreign_key="product.id", nullable=False)
    fedapay_id: str = Field()
