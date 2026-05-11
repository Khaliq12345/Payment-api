import os

import httpx
from dotenv import load_dotenv

load_dotenv()


class Whatsapp:
    def __init__(self) -> None:
        self.whatsappInstance = os.getenv("WhatsappInstance")
        self.url = os.getenv("WHATSAPP_URL")
        self.token = os.getenv("WHATSAPP_TOKEN")
        self.headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            "X-Api-Key": self.token,
        }

    def check_whatsapp(self, number: int) -> dict:
        """verify if a whatsapp number is available"""
        response = httpx.get(
            f"{self.url}/api/contacts/check-exists?phone={number}&session=default",
            headers=self.headers,
        )
        output = response.json()
        return {"existsWhatsapp": output.get("numberExists")}

    def get_chats(self) -> list[dict]:
        """Get all whatsapp groups"""
        params = {
            "exclude": "participants",
        }
        url = f"{self.url}/api/default/groups"
        response = httpx.get(url, params=params, headers=self.headers)
        return response.json()

    def add_to_group(self, groupId: str, phone: str):
        """Add user to group"""
        url = f"{self.url}/api/default/groups/{groupId}%40g.us/participants/add"
        json_data = {
            "participants": [
                {
                    "id": f"{phone}@c.us",
                },
            ],
        }
        response = httpx.post(url, json=json_data, headers=self.headers)
        response.raise_for_status()
        return response.json()
