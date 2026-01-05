import os

from dotenv import load_dotenv

load_dotenv()


BASE_DOMAIN: str = os.getenv("BASE_DOMAIN", "http://localhost:3000")
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
