from tokenize import group

from fastapi import APIRouter
from fastapi.params import Query

from src.services.whatsapp import Whatsapp

router = APIRouter(prefix="/api/whatsapp", tags=["WHATSAPP"])


@router.get("/verify")
def verify_number(number: int):
    whatsapp = Whatsapp()
    return whatsapp.check_whatsapp(number)


@router.get("/chats")
def get_chats():
    whatapp = Whatsapp()
    return whatapp.get_chats()


@router.get("/add")
def add_user_to_group(groupId: int, phone: int):
    whatsapp = Whatsapp()
    return whatsapp.add_to_group(groupId, phone)
