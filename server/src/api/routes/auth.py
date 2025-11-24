import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["AUTHENTICATE"])

# Identifiants depuis .env
ENV_USERNAME = os.getenv("AUTH_USERNAME")
ENV_PASSWORD = os.getenv("AUTH_PASSWORD")


class TokenResponse(BaseModel):
    login: bool


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Vérification simple du login via OAuth2PasswordRequestForm"""

    # 1. Vérifier si les variables sont dans l'environnement
    if not ENV_USERNAME or not ENV_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AUTH_USERNAME or AUTH_PASSWORD missing in .env",
        )

    # 2. Vérifier les identifiants envoyés
    if form_data.username != ENV_USERNAME or form_data.password != ENV_PASSWORD:
        return TokenResponse(login=False)

    # 3. Succès
    return TokenResponse(login=True)
