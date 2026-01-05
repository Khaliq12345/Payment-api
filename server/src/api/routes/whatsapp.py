from fastapi import APIRouter, HTTPException

from src.api.dependencies import fedapayDepends
from src.services.whatsapp import Whatsapp
from src.utils.utils import get_group_amount

router = APIRouter(prefix="/api/whatsapp", tags=["WHATSAPP"])


@router.get("/verify")
def verify_number(number: int):
    """
    Vérifie si un numéro est actif sur WhatsApp
    """
    try:
        whatsapp = Whatsapp()
        is_active = whatsapp.check_whatsapp(number)
        return is_active
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error while verifying number: {str(e)}"
        )


@router.get("/chats")
def get_chats():
    try:
        whatsapp = Whatsapp()
        chats = whatsapp.get_chats()

        # Filtrer uniquement les chats avec un "name"
        chats = [chat for chat in chats if "name" in chat]

        # Ajouter le montant pour chaque groupe
        for chat in chats:
            group_id = chat["id"]
            try:
                chat["amount"] = get_group_amount(group_id)
            except Exception:
                chat["amount"] = 0  # Par défaut 0 si impossible de récupérer le montant

        return chats

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error while retrieving chats: {str(e)}"
        )


@router.post("/add")
def add_user_to_group(fedapayDepends: fedapayDepends, transaction_id: int):
    """
    Ajouter un utilisateur à un groupe WhatsApp
    """
    try:
        whatsapp = Whatsapp()
        transaction = fedapayDepends.get_transaction(transactionId=transaction_id)
        if not transaction.group_id:
            raise HTTPException(
                status_code=403,
                detail="Error groupid is missing",
            )
        result = whatsapp.add_to_group(
            groupId=transaction.group_id, phone=transaction.whatsapp_phone
        )
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error while adding user to group: {str(e)}",
        )
