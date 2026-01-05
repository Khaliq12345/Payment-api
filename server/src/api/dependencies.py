from typing import Annotated

from fastapi import Depends

from src.services.drive import GoogleAutomation
from src.services.email_service import Email
from src.services.fedapay import FedaPay
from src.storage.database import Database

# Dépendance pour la base de données
databaseDepends = Annotated[Database, Depends(Database)]
emailDepends = Annotated[Email, Depends(Email)]
googleDepends = Annotated[GoogleAutomation, Depends(GoogleAutomation)]
fedapayDepends = Annotated[FedaPay, Depends(FedaPay)]
