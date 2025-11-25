from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from src.schema import Customer, Transaction
from src.services.fedapay import FedaPay
from src.utils.utils import add_user, get_user

router = APIRouter(prefix="/api/fedapay", tags=["FEDAPAY"])


@router.post("/create-customer")
def create_customer(customer: Customer):
    try:
        customer_dict = jsonable_encoder(customer)
        fedapay = FedaPay()

        # Vérifier si user existe déjà
        customer_info = get_user(customer.email)
        customer_id = customer_info.get("user_id") if customer_info else None

        if customer_id:
            response = fedapay.retrieve_customer(customer_id)
        else:
            response = fedapay.create_customer(customer_dict)

        # Vérifier la réponse FedaPay
        customer_data = response["v1/customer"]
        if not customer_data:
            raise HTTPException(
                status_code=500, detail="Erreur lors de la création du user"
            )

        # Sauvegarde local DB / fichier
        add_user(customer.email, customer_data["id"], customer.phone_number)

        return response

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/get-customer")
def get_customer(email: str):
    try:
        customer = get_user(email)
        if not customer:
            raise HTTPException(
                status_code=404, detail=f"User with email '{email}' not found"
            )

        customer_id = customer.get("user_id")
        if not customer_id:
            raise HTTPException(
                status_code=404, detail=f"User ID not found for email '{email}'"
            )

        fedapay = FedaPay()
        response = fedapay.retrieve_customer(customer_id)
        customer_data = response["v1/customer"]

        if not customer_data:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la récupération du customer depuis FedaPay",
            )

        return customer_data

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/transaction")
def create_transaction(transaction: Transaction):
    try:
        transaction_dict = jsonable_encoder(transaction)
        fedapay = FedaPay()
        response = fedapay.create_transaction(transaction_dict)
        return response

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/transaction")
def get_transaction(transactionId: str):
    try:
        fedapay = FedaPay()
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
