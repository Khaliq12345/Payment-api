from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.api.dependencies import databaseDepends
from src.schema import ProductCreate


router = APIRouter(prefix="/api/products", tags=["PRODUCTS"])


@router.post("/add")
def add_product(
    payload: ProductCreate,
    db: databaseDepends,
):
    try:
        product = db.add_product(
            title=payload.title,
            description=payload.description,
            price=float(payload.price),
            platform=payload.platform,
        )
        return {"id": product.id, "url": product.url}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while creating product: {str(e)}",
        )


@router.get("/")
def list_products(
    db: databaseDepends,
    page: int = 1,
    page_size: int = 10,
    platform: str | None = None,
    name: str | None = None,
    date_filter: datetime | None = None,
):
    try:
        products = db.get_products(
            page=page,
            page_size=page_size,
            platform=platform,
            name=name,
            created_date=date_filter,
        )
        return products

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while listing products: {str(e)}",
        )


@router.get("/{product_id}")
def get_product(
    product_id: str,
    db: databaseDepends,
):
    try:
        product = db.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while retrieving product: {str(e)}",
        )


@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: databaseDepends,
):
    try:
        # Vérifier que le produit existe 
        product = db.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        db.delete_product(product_id)
        return None

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while deleting product: {str(e)}",
        )

