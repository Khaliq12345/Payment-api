from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/auth", tags=["AUTHENTICATE"])

# Identifiants dans .env
ENV_USERNAME = os.getenv("AUTH_USERNAME")
ENV_PASSWORD = os.getenv("AUTH_PASSWORD")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Auth simplifiée — identique à la doc FastAPI mais
    avec vérification simple via .env
    """

    if not ENV_USERNAME or not ENV_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AUTH_USERNAME or AUTH_PASSWORD missing in .env"
        )

    # Vérification simple
    if form_data.username != ENV_USERNAME or form_data.password != ENV_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    # On retourne un token simple comme dans la doc
    return TokenResponse(access_token=form_data.username)
