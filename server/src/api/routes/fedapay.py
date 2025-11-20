from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from src.schema import Customer, Transaction
from src.services.fedapay import FedaPay

router = APIRouter(prefix="/api/fedapay", tags=["FEDAPAY"])


@router.post("/create-customer")
def create_customer(customer: Customer):
    customer_dict = jsonable_encoder(customer)
    fedapay = FedaPay()
    response = fedapay.create_customer(customer_dict)

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
