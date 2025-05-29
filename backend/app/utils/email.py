import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor


class EmailSender:
    def __init__(
        self,
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 587,
        email_user: str = "aummataliy@gmail.com",
        email_password: str = "wievsjqxyvqzawpp"
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_user = email_user
        self.email_password = email_password
        self.executor = ThreadPoolExecutor(max_workers=3)

    def _send_email_sync(self, to_email: str, subject: str, text: str) -> bool:
        """Sinxron email yuborish"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg['Subject'] = subject

            msg.attach(MIMEText(text, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            text_content = msg.as_string()
            server.sendmail(self.email_user, to_email, text_content)
            server.quit()

            print(f"Xabar muvaffaqiyatli yuborildi: {to_email}")
            return True
        except Exception as error:
            print(f"Email yuborishda xatolik: {error}")
            return False

    async def send_email(self, to_email: str, subject: str, text: str) -> bool:
        """Asinxron email yuborish"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._send_email_sync,
            to_email,
            subject,
            text
        )


# Global email sender instance
email_sender = EmailSender()


async def send_to_email(email: str, subject: str, text: str) -> bool:
    """Email yuborish funksiyasi"""
    return await email_sender.send_email(email, subject, text)
