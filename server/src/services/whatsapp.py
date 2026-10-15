import os

import httpx
from dotenv import load_dotenv

from src.storage.database import Database

load_dotenv()


class Whatsapp:
    def __init__(self, email: str) -> None:
        self.db = Database()
        self.whatsappInstance = os.getenv("WhatsappInstance")
        self.url = os.getenv("WHATSAPP_URL")
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.session = self.db.get_whatsapp_token(email)
        self.headers = {
            "accept": "application/json",
            "X-API-Key": self.token,
            "Content-Type": "application/json",
        }

    def check_whatsapp(self, number: int) -> dict:
        """verify if a whatsapp number is available"""
        url = f"{self.url}/api/sessions/{self.session}/contacts/check/{number}"
        response = httpx.get(url, headers=self.headers)
        json_data = response.json()
        return json_data["exists"]

    def get_chats(self) -> list[dict]:
        """Get all whatsapp chat"""
        url = f"{self.url}/api/sessions/{self.session}/groups"
        response = httpx.get(url, headers=self.headers)
        return response.json()

    def add_to_group(self, groupId: str, phone: str):
        """Add user to group"""
        json_data = {
            "participants": [
                f"{phone}@c.us",
            ],
        }
        url = f"{self.url}/api/sessions/{self.session}/groups/{groupId}/participants"
        response = httpx.post(url, json=json_data, headers=self.headers)
        response.raise_for_status()
        return response.json()
