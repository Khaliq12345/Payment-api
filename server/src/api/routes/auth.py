import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["AUTHENTICATE"])

# Identifiants dans .env
ENV_USERNAME = os.getenv("AUTH_USERNAME")
ENV_PASSWORD = os.getenv("AUTH_PASSWORD")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Auth simplifiée avec format standard et gestion des erreurs"""
    try:
        if not ENV_USERNAME or not ENV_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AUTH_USERNAME or AUTH_PASSWORD missing in .env",
            )

        if form_data.username != ENV_USERNAME or form_data.password != ENV_PASSWORD:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
            )

        # Retour formaté
        return {
            "status": 200,
            "message": "Login successful",
            "data": {"access_token": form_data.username, "token_type": "bearer"},
        }

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
