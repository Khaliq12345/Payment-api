import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class Whatsapp:
    def __init__(self) -> None:
        self.whatsappInstance = os.getenv("WhatsappInstance")
        self.url = "https://7107.api.green-api.com"
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.headers = {
            "Content-Type": "application/json",
        }

    def check_whatsapp(self, number: int) -> dict:
        """verify if a whatsapp number is available"""
        url = f"{self.url}/{self.whatsappInstance}/checkWhatsapp/{self.token}"
        payload = {"phoneNumber": number}
        response = httpx.post(url, json=payload)
        return response.json()

    def get_chats(self) -> list[dict]:
        """Get all whatsapp chat"""
        url = f"{self.url}/{self.whatsappInstance}/getChats/{self.token}"
        response = httpx.get(url)
        return response.json()

    def add_to_group(self, groupId: int, phone: int):
        """Add user to group"""
        url = f"{self.url}/{self.whatsappInstance}/addGroupParticipant/{self.token}"
        payload = {
            "groupId": f"{groupId}@g.us",
            "participantChatId": f"{phone}@c.us",
        }
        response = httpx.post(url, json=payload, headers=self.headers)
        return response.json()
