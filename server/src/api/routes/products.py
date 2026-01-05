from datetime import datetime

from fastapi import APIRouter, HTTPException

from src.api.dependencies import databaseDepends
from src.model import Customer
from src.schema import ProductCreate

router = APIRouter(prefix="/api/products", tags=["PRODUCTS"])


@router.post("/add")
def add_product(
    payload: ProductCreate,
    db: databaseDepends,
):
    print(payload)
    try:
        if (payload.platform.value == "whatsapp") and (not payload.whatsapp_groupid):
            raise HTTPException(
                detail="Whatasapp GroupID is needed for platform whatsapp",
                status_code=403,
            )
        if (payload.platform.value == "email") and (not payload.drive_link):
            raise HTTPException(
                detail="Drive link is needed for platform email", status_code=403
            )
        product_id = db.add_product(payload)
        return {"id": product_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        print(str(e))
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
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    price: int | None = None,
):
    try:
        products = db.get_products(
            page=page,
            page_size=page_size,
            platform=platform,
            name=name,
            created_date=start_date,
            end_date=end_date,
            price=price,
        )
        return products

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while listing products: {str(e)}",
        )


@router.get("/customers")
def list_customers(db: databaseDepends, product_id: str) -> list[Customer]:
    """List all customers of a particular product"""
    try:
        customers = db.get_customers(product_id)
        return customers
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


@router.post("/update")
def edit_product(db: databaseDepends, product_id: str, product_info: dict):
    try:
        print(product_info)
        title = product_info.get("title")
        description = product_info.get("description")
        price = product_info.get("price")
        product = db.edit_product(product_id, title, description, price)
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


@router.delete("/delete")
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
