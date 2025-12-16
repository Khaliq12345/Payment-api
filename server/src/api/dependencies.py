from typing import Annotated

from fastapi import Depends

from src.storage.database import Database


# Dépendance pour la base de données
databaseDepends = Annotated[Database, Depends(Database)]


