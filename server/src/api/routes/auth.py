from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from src.api.dependencies import databaseDepends

router = APIRouter(prefix="/api/auth", tags=["AUTHENTICATE"])


class TokenResponse(BaseModel):
    login: bool


@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    db: databaseDepends,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """Vérification du login depuis la table Users"""

    is_logged_in = db.is_user_info_correct(form_data.username, form_data.password)
    if not is_logged_in:
        return TokenResponse(login=False)

    # 3. Succès
    return TokenResponse(login=True)
