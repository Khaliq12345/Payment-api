from fastapi import FastAPI

from src.api.routes.auth import router as auth_router
from src.api.routes.fedapay import router as fedapay_router
from src.api.routes.products import router as products_router
from src.api.routes.whatsapp import router as whatsapp_router
from src.api.routes.email import router as email_router
from src.storage.database import Database
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = Database()
    # --- Startup ---
    db.create_database()
    print("Database tables created successfully!")
    yield


# 3. Pass lifespan to your FastAPI app
app = FastAPI(lifespan=lifespan)

app.include_router(whatsapp_router)
app.include_router(fedapay_router)
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(email_router)
