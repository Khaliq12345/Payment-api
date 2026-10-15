from datetime import datetime
from typing import Any, Dict, Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Column, Field, SQLModel


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
    media_url: Optional[str]
    user_email: str


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


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password: str
    whatsapp_access: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSONB)
    )
    fedapay_access: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSONB)
    )
