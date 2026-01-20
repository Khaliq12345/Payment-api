import os

from dotenv import load_dotenv

load_dotenv()


BASE_DOMAIN: str = os.getenv("BASE_DOMAIN", "http://localhost:3000")
GOOGLE_APP_PASSWORD = os.getenv("GOOGLE_APP_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")
ENV = os.getenv("ENV")
