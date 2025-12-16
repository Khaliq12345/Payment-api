import os
import secrets
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sqlmodel import Session, SQLModel, create_engine, select

from src.config import BASE_DOMAIN
from src.model import Product


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
    def add_product(
        self,
        title: str,
        description: str,
        price: float,
        platform: str,
    ) -> Product:
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
                title=title,
                description=description,
                price=price,
                platform=platform,
                url=f"{BASE_DOMAIN.rstrip('/')}/project/{product_id}",
                created_at=created_at,
            )
            session.add(product)
            session.commit()
            session.refresh(product)

            return product

    def get_products(
        self,
        page: int = 1,
        page_size: int = 10,
        platform: Optional[str] = None,
        name: Optional[str] = None,
        created_date: Optional[datetime] = None,
    ) -> list[Product]:
        """
        Récupère une liste de produits avec pagination et filtres.
        """
        with Session(self.engine) as session:
            stmt = select(Product)

            if platform:
                stmt = stmt.where(Product.platform == platform)

            if name:
                stmt = stmt.where(Product.title.contains(name))

            if created_date:
                stmt = stmt.where(Product.created_at == created_date)

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
