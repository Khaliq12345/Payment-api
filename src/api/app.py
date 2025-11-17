from fastapi import FastAPI

from src.api.routes.fedapay import router as fedapay_router
from src.api.routes.whatsapp import router as whatsapp_router

app = FastAPI()

app.include_router(whatsapp_router)
app.include_router(fedapay_router)
