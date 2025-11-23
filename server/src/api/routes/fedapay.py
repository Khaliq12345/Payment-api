from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from src.schema import Customer, Transaction
from src.services.fedapay import FedaPay
from src.utils.utils import add_user, get_user

router = APIRouter(prefix="/api/fedapay", tags=["FEDAPAY"])


@router.post("/create-customer")
def create_customer(customer: Customer):
    customer_dict = jsonable_encoder(customer)
    fedapay = FedaPay()

    customer_info = get_user(customer.email)
    customer_id = customer_info.get("user_id")
    if customer_id:
        response = fedapay.retrieve_customer(customer_id)
    else:
        response = fedapay.create_customer(customer_dict)
    customer_data = response.get("v1/customer")
    if not customer_data:
        raise HTTPException(
            detail="Erreur lors de la creation du user", status_code=500
        )
    add_user(customer.email, customer_data["id"], customer.phone_number)
    return response


@router.get("/get-customer")
def get_customer(email: str):
    """Endpoint to retrieve customer info"""
    customer = get_user(email)
    print(customer)
    customer_id = customer.get("user_id")
    if not customer_id:
        raise HTTPException(status_code=404, detail="User not found")
    customer_phone = customer.get("number")
    if not customer_phone:
        return {}
    fedapay = FedaPay()
    response = fedapay.retrieve_customer(customer_id)
    return response


@router.post("/transaction")
def create_transaction(transaction: Transaction):
    transaction_dict = jsonable_encoder(transaction)
    fedapay = FedaPay()
    response = fedapay.create_transaction(transaction_dict)
    return response


@router.get("/transaction")
def get_transaction(transactionId: str):
    fedapay = FedaPay()
    response = fedapay.get_transaction(transactionId)
    return response
