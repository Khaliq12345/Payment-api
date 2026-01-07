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
            # Professional HTML Template - French
            html_body = f"""
                <html>
                <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
                    <div style="max-width: 600px; margin: 20px auto; border: 1px solid #e0e0e0; border-radius: 10px; overflow: hidden;">
                        <div style="background-color: #4285F4; padding: 20px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 22px;">Action Requise : Confirmez Votre Appel</h1>
                        </div>
                        <div style="padding: 30px;">
                            <p>Bonjour,</p>
                            <p>Merci d'avoir réservé <strong>{title}.</strong></p>

                            <div style="background-color: #fff4e5; border-left: 4px solid #ffa117; padding: 15px; margin: 20px 0;">
                                <p style="margin: 0; font-weight: bold; color: #855d00;">Étape Importante Suivante :</p>
                                 <a href="{event_link}" style="background-color: #34a853; color: white; padding: 14px 28px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Lien d'Invitation au Calendrier</a>
                                <p style="margin: 5px 0 0 0;">Veuillez ouvrir l'invitation Google Calendar et cliquer sur <strong>"Oui"</strong> pour confirmer votre présence. Cela garantit que le lien reste sur votre calendrier.</p>
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
                            <h1 style="color: white; margin: 0; font-size: 22px;">Succès ! Vos Fichiers Sont Prêts</h1>
                        </div>
                        <div style="padding: 30px;">
                            <p>Bonjour,</p>
                            <p>Merci pour votre achat. Vous pouvez maintenant accéder à <strong>{title}</strong> directement via Google Drive en utilisant le bouton ci-dessous :</p>

                            <div style="text-align: center; margin: 30px 0;">
                                <a href="{drive_link}" style="background-color: #34a853; color: white; padding: 14px 28px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Accéder à Votre Produit</a>
                            </div>

                            <p style="font-size: 13px; color: #666; border-top: 1px solid #eee; padding-top: 15px;">
                                <strong>Exigence :</strong> Vous devez être connecté à <b>{receiver_email}</b> pour voir ces fichiers.
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
