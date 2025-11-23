from fastapi import APIRouter

from src.services.whatsapp import Whatsapp
from src.utils.utils import get_group_amount, update_group_amount

router = APIRouter(prefix="/api/whatsapp", tags=["WHATSAPP"])


@router.get("/verify")
def verify_number(number: int):
    whatsapp = Whatsapp()
    return whatsapp.check_whatsapp(number)


@router.get("/chats")
def get_chats():
    whatapp = Whatsapp()
    chats = whatapp.get_chats()
    # Filter chats to only include those with a "name" key
    chats = [chat for chat in chats if "name" in chat]
    for chat in chats:
        group_id = chat["id"]
        chat["amount"] = get_group_amount(group_id)
    return chats


@router.post("/add")
def add_user_to_group(groupId: str, phone: int):
    whatsapp = Whatsapp()
    return whatsapp.add_to_group(groupId, phone)


@router.post("/update-group-amount")
def update_whatsapp_group_amount(group_id: str, amount: float | int):
    """Update the amount for a whatsapp group"""
    update_group_amount(group_id, amount)
