from hmac import trans_5C

from fastapi import APIRouter, HTTPException

from src.api.dependencies import emailDepends, fedapayDepends, googleDepends

router = APIRouter(prefix="/api/email", tags=["EMAIL"])


@router.post("/send")
def send_email(
    emailDepends: emailDepends,
    fedapayDepends: fedapayDepends,
    googleDepends: googleDepends,
    transaction_id: int,
):
    """
    Send the user an email
    """
    try:
        transaction = fedapayDepends.get_transaction(transactionId=transaction_id)
        print(transaction)
        if not transaction.drive_link:
            raise HTTPException(status_code=404, detail="No material provided")
        if "calendar.app.google" in transaction.drive_link:
            send_type = "meeting"
        elif "drive.google.com" in transaction.drive_link:
            send_type = "document"
        else:
            print(transaction.drive_link)
            raise HTTPException(
                status_code=404, detail="No valid material provided; contact the owner"
            )

        match send_type:
            case "document":
                googleDepends.add_permission_to_drive_file(
                    transaction.email, transaction.drive_link
                )
                emailDepends.send_email(
                    send_type_str=send_type,
                    receiver_email=transaction.email,
                    title=transaction.title,
                    drive_link=transaction.drive_link,
                )
            case "meeting":
                emailDepends.send_email(
                    send_type_str=send_type,
                    receiver_email=transaction.email,
                    title=transaction.title,
                    event_link=transaction.drive_link,
                )
        return {"detail": "email sent"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error while verifying number: {str(e)}"
        )
