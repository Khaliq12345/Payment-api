import os
from math import e

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
        print(groupId, phone)
        url = f"{self.url}/api/default/groups/{groupId}%40g.us/participants/add"
        print(url)
        json_data = {
            "participants": [
                {
                    "id": f"{phone}@c.us",
                },
            ],
        }

        try:
            print(json_data)
            response = httpx.post(url, json=json_data, headers=self.headers)
            print(response)
            return response.json()
        except httpx.HTTPStatusError as e:
            # THIS IS THE KEY: It prints the actual error message from the WAHA server
            print(f"!!! SERVER ERROR (500): {e.response.text}")
            return {"error": True, "details": e.response.text}
        except Exception as e:
            print(f"!!! REQUEST FAILED: {e}")
            return None
