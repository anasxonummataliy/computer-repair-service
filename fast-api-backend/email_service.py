import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

# Email settings
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USER = "hojiakbarnasriddinov2006@gmail.com"
EMAIL_PASSWORD = "wievsjqxyvqzawpp"

async def send_email(email: str, subject: str, text: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(text, 'plain'))
        
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text_content = msg.as_string()
        server.sendmail(EMAIL_USER, email, text_content)
        server.quit()
        print(f"Xabar yuborildi: {email}")
    except Exception as error:
        print(f"Email yuborishda xatolik: {error}")
        raise HTTPException(status_code=500, detail="Email yuborishda xatolik")
