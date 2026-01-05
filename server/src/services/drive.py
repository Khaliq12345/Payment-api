from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleAutomation:
    def __init__(self) -> None:
        self.credentials = service_account.Credentials.from_service_account_file(
            "cred.json"
        )

        scoped_credentials = self.credentials.with_scopes(
            [
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/calendar",
            ]
        )
        self.credentials = scoped_credentials

    def add_permission_to_drive_file(self, email: str, file_link: str) -> bool:
        """Add a new permission to a file in google drive"""
        file_id = file_link.split("/")[-1].split("?")[0]
        service = build("drive", "v3", credentials=self.credentials)

        user_permission = {
            "type": "user",
            "role": "reader",
            "emailAddress": email,
        }
        service.permissions().create(
            fileId=file_id, body=user_permission, sendNotificationEmail=True
        ).execute()
        print("PERMISSION ADDED!!")
        return True
