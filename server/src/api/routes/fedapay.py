from fastapi import APIRouter, HTTPException

from src.api.dependencies import databaseDepends
from src.schema import Customer, Transaction
from src.services.fedapay import FedaPay

router = APIRouter(prefix="/api/fedapay", tags=["FEDAPAY"])


@router.post("/create-customer")
def create_customer(db: databaseDepends, customer: Customer, user_email: str):
    try:
        fedapay = FedaPay(user_email)
        # Vérifier si user existe déjà
        user_exists = db.verify_if_customer_in_db(customer.email, customer.product_id)
        if user_exists:
            customer_info = db.retrieve_customer(
                product_id=customer.product_id, email=customer.email
            )
            if not customer_info:
                raise HTTPException(status_code=404, detail="Client non trouvee")
            response = fedapay.retrieve_customer(customer_info.fedapay_id)
        else:
            response = fedapay.create_customer(customer)
            db.add_customer(customer, response["id"], customer.product_id)
        return response
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


# @router.get("/get-customer")
# def get_customer(email: str, user_email: str, db: databaseDepends):
#     try:
#         db.retrieve_customer()
#         customer = get_user(email)
#         if not customer:
#             raise HTTPException(
#                 status_code=404, detail=f"User with email '{email}' not found"
#             )
#
#         customer_id = customer.get("user_id")
#         if not customer_id:
#             raise HTTPException(
#                 status_code=404, detail=f"User ID not found for email '{email}'"
#             )
#
#         fedapay = FedaPay(user_email)
#         response = fedapay.retrieve_customer(customer_id)
#         customer_data = response["v1/customer"]
#
#         if not customer_data:
#             raise HTTPException(
#                 status_code=500,
#                 detail="Erreur lors de la récupération du customer depuis FedaPay",
#             )
#
#         return customer_data
#
#     except HTTPException as http_err:
#         raise http_err
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/transaction")
def create_transaction(
    customer_id: str, product_id: str, callback_url: str, user_email: str
) -> dict:
    """Create a new transaction and retrieve it's url"""
    try:
        print(customer_id, product_id, callback_url)
        fedapay = FedaPay(user_email)
        response = fedapay.create_transaction(
            customer_id=customer_id, product_id=product_id, callback_url=callback_url
        )
        if not response:
            raise HTTPException(
                status_code=404, detail="Customer or Product not available"
            )
        return {"payment_link": response}

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/transaction")
def get_transaction(transactionId: str, user_email: str) -> Transaction:
    try:
        fedapay = FedaPay(user_email)
        response = fedapay.get_transaction(transactionId)
        if not response:
            raise HTTPException(
                status_code=404,
                detail=f"Transaction with ID '{transactionId}' not found",
            )

        return response

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
