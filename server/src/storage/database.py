import os
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Optional

from sqlmodel import Session, SQLModel, create_engine, select

from src.model import Product


class Database:

    def __init__(self) -> None:
        # Base de données SQLite stockée dans server/src/storage/app.db
        storage_dir = Path(__file__).resolve().parent
        db_path = storage_dir / "app.db"
        db_url = f"sqlite:///{db_path}"
        self.engine = create_engine(db_url)
        
        # Création automatique de la base et des tables au startup
        self.create_database()

    def create_database(self):
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
        Ajoute un produit, génère l'URL et retourne l'objet Product.
        """
        with Session(self.engine) as session:
            created_at = datetime.now(tz=timezone.utc)

            product = Product(
                title=title,
                description=description,
                price=price,
                platform=platform,
                url="", 
                created_at=created_at,
            )
            session.add(product)
            session.commit()
            session.refresh(product)

            base_domain = os.getenv("BASE_DOMAIN", "http://localhost:3000")
            product.url = f"{base_domain.rstrip('/')}/project/{product.id}"
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
        created_date: Optional[date] = None,
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
                start_dt = datetime.combine(created_date, time.min).replace(
                    tzinfo=timezone.utc
                )
                end_dt = datetime.combine(created_date, time.max).replace(
                    tzinfo=timezone.utc
                )
                stmt = stmt.where(Product.created_at.between(start_dt, end_dt))

            offset = (page - 1) * page_size
            stmt = stmt.offset(offset).limit(page_size)

            results = session.exec(stmt).all()
            return list(results)

    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Récupère un produit par son id.
        """
        with Session(self.engine) as session:
            stmt = select(Product).where(Product.id == product_id)
            return session.exec(stmt).first()

    def delete_product(self, product_id: int) -> None:
        """
        Supprime un produit par son id.
        """
        with Session(self.engine) as session:
            product = session.get(Product, product_id)
            if product:
                session.delete(product)
                session.commit()


# Instance globale de la base de données
db = Database()
