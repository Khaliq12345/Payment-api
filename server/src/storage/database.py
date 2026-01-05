import json
import secrets
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from dateparser import parse, parser
from sqlmodel import Session, SQLModel, create_engine, or_, select

from src.model import Customer, Product
from src.schema import Customer as CustomerSchema
from src.schema import ProductCreate

# TODO
# 1. Fix the get_products filters


class Database:
    def __init__(self) -> None:
        # Base de données SQLite stockée dans server/src/storage/app.db
        storage_dir = Path(__file__).resolve().parent
        db_path = storage_dir / "app.db"
        db_url = f"sqlite:///{db_path}"
        self.engine = create_engine(db_url)

        # Création automatique de la base et des tables au démarrage
        self.create_database()

    def create_database(self) -> None:
        """Crée les tables de la base de données si elles n'existent pas."""
        SQLModel.metadata.create_all(self.engine)

    # Products
    def add_product(self, product_info: ProductCreate) -> str | None:
        """
        Ajoute un produit et retourne l'objet Product.
        """
        with Session(self.engine) as session:
            created_at = datetime.now(tz=timezone.utc)

            # Génération de l'id unique à partir d'un random + timestamp
            random_part = secrets.token_hex(8)
            timestamp_part = int(time.time())
            product_id = f"{random_part}{timestamp_part}"

            product = Product(
                id=product_id,
                created_at=created_at,
                title=product_info.title,
                description=product_info.description,
                price=product_info.price,
                platform=product_info.platform.value,
                drive_link=product_info.drive_link,
                whatsapp_groupid=product_info.whatsapp_groupid,
            )
            session.add(product)
            session.commit()
            return product_id

    def get_products(
        self,
        page: int = 1,
        page_size: int = 10,
        platform: Optional[str] = None,
        name: Optional[str] = None,
        created_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        price: int | None = None,
    ) -> list[Product]:
        """
        Récupère une liste de produits avec pagination et filtres.
        """
        with Session(self.engine) as session:
            stmt = select(Product)

            if (platform) and (platform != "all") and (platform != "All"):
                stmt = stmt.where(Product.platform == platform)

            if name:
                stmt = stmt.where(Product.title.contains(name))

            if price:
                stmt = stmt.where(Product.price == price)

            if created_date:
                stmt = stmt.where(Product.created_at >= created_date)

            if end_date:
                end = end_date + timedelta(days=1)
                stmt = stmt.where(Product.created_at < end)

            offset = (page - 1) * page_size
            stmt = stmt.offset(offset).limit(page_size)

            results = session.exec(stmt).all()
            return list(results)

    def get_product(self, product_id: str) -> Optional[Product]:
        """
        Récupère un produit par son id.
        """
        with Session(self.engine) as session:
            stmt = select(Product).where(Product.id == product_id)
            return session.exec(stmt).first()

    def delete_product(self, product_id: str) -> None:
        """
        Supprime un produit par son id.
        """
        with Session(self.engine) as session:
            product = session.get(Product, product_id)
            if product:
                session.delete(product)
                session.commit()

    def edit_product(
        self,
        product_id: str,
        title: str | None,
        description: str | None,
        price: float | None,
    ) -> Product | None:
        """
        Modifie un produit par son id.
        """
        product_data = None
        with Session(self.engine) as session:
            product = session.get(Product, product_id)
            if product:
                if title:
                    product.title = title
                if description:
                    product.description = description
                if price:
                    product.price = price
                product_data = json.loads(product.model_dump_json())
                session.add(product)
                session.commit()
        return product_data

    # -----------CUSTOMER--------------------------
    def get_customers(self, product_id: str) -> list[Customer]:
        """Retrieve all customers for a particular product"""
        with Session(self.engine) as session:
            stmt = select(Customer).where(Customer.product_id == product_id)
            records = session.exec(stmt).fetchall()
            return list(records)

    def add_customer(
        self, customer_data: CustomerSchema, fedapay_id: str, product_id: str
    ) -> Customer:
        """Add a new customer to the db"""
        with Session(self.engine) as session:
            # Add new customer
            customer_id = f"cust-{fedapay_id}-{product_id}"
            customer_new = Customer(
                id=customer_id,
                first_name=customer_data.first_name,
                last_name=customer_data.last_name,
                email=customer_data.email,
                phone=customer_data.phone,
                whatsapp_phone=customer_data.whatsapp_phone,
                country=customer_data.country.value,
                product_id=customer_data.product_id,
                fedapay_id=fedapay_id,
            )
            session.add(customer_new)
            session.commit()
            return customer_new

    def retrieve_customer(
        self, product_id: str, email: str | None = None, customer_id: str | None = None
    ) -> Customer | None:
        """Get a customer from the database"""
        with Session(self.engine) as session:
            stmt = (
                select(Customer)
                .where(or_(Customer.email == email, Customer.fedapay_id == customer_id))
                .where(Customer.product_id == product_id)
            )
            customer = session.exec(stmt).first()
            return customer

    def verify_if_customer_in_db(self, email: str, product_id: str) -> bool:
        """Verify if the customer is in database"""
        with Session(self.engine) as session:
            stmt = select(Customer).where(
                Customer.email == email, Customer.product_id == product_id
            )
            customer = session.exec(stmt).first()
            if customer:
                return True
            return False
