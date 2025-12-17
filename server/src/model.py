from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    # Id généré manuellement
    id: str = Field(primary_key=True)
    title: str
    description: str
    price: float
    platform: str
    url: str
    created_at: datetime

