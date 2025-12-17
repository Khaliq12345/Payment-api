from dotenv import load_dotenv
import os

load_dotenv()


BASE_DOMAIN: str = os.getenv("BASE_DOMAIN", "http://localhost:3000")




