import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from enum import Enum

from src.config import GOOGLE_APP_PASSWORD, SENDER_EMAIL


class SendingType(Enum):
    meeting = "meeting"
    materials = "document"


class Email:
    def __init__(self) -> None:
        self.sender_email = SENDER_EMAIL
        self.subject = "Your Digital Access & Meeting Details"
        self.password = GOOGLE_APP_PASSWORD

    def send_email(
        self,
        send_type_str: str,
        receiver_email: str,
        title: str,
        event_link: str | None = None,
        drive_link: str | None = None,
    ) -> bool:
        send_type = SendingType(send_type_str)
        message = MIMEMultipart("alternative")
        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = self.subject

        if (send_type.value == "meeting") and (event_link):
            # Professional HTML Template
            html_body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 20px auto; border: 1px solid #e0e0e0; border-radius: 10px; overflow: hidden;">
                        <div style="background-color: #4285F4; padding: 20px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 22px;">Action Required: Confirm Your Call</h1>
                        </div>
                        <div style="padding: 30px;">
                            <p>Hello,</p>
                            <p>Thank you for booking <strong>{title}.</strong></p>

                            <div style="background-color: #fff4e5; border-left: 4px solid #ffa117; padding: 15px; margin: 20px 0;">
                                <p style="margin: 0; font-weight: bold; color: #855d00;">Important Next Step:</p>
                                 <a href="{event_link}" style="background-color: #34a853; color: white; padding: 14px 28px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Calendar invitation Link</a>
                                <p style="margin: 5px 0 0 0;">Please open the Google Calendar invitation and click <strong>"Yes"</strong> to confirm your attendance. This ensures the link stays on your calendar.</p>
                            </div>
                        </div>
                    </div>
                </body>
                </html>
            """
        elif (send_type.value == "document") and (drive_link):
            html_body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 20px auto; border: 1px solid #e0e0e0; border-radius: 10px; overflow: hidden;">
                        <div style="background-color: #34a853; padding: 20px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 22px;">Success! Your Files are Ready</h1>
                        </div>
                        <div style="padding: 30px;">
                            <p>Hello,</p>
                            <p>Thank you for your purchase. You can now access <strong>{title}</strong> directly via Google Drive using the button below:</p>

                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{drive_link}" style="background-color: #34a853; color: white; padding: 14px 28px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Access Your Product</a>
                            </div>

                            <p style="font-size: 13px; color: #666; border-top: 1px solid #eee; padding-top: 15px;">
                                <strong>Requirement:</strong> You must be logged into <b>{receiver_email}</b> to view these files.
                            </p>
                        </div>
                    </div>
                </body>
                </html>
            """
        else:
            return False

        # Attach HTML version
        message.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.password)
            server.send_message(message)

        success_message = "EMAIL SENT SUCCESSFULLY"
        print(success_message)
        return True
