from fastapi import FastAPI
import smtplib
from pydantic import BaseModel
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_APPLICATION = os.getenv('EMAIL_APPLICATION')
PASSWORD_APPLICATION = os.getenv('PASSWORD_APPLICATION')

class EmailStr(BaseModel):
    subject: str
    originEmail: str
    message: str
#Auth
app = FastAPI()

@app.post('/send-email')
async def send_email(email: EmailStr):
    msg = EmailMessage()
    msg['Subject'] = email.subject
    msg['From'] = EMAIL_APPLICATION
    msg['To'] = EMAIL_APPLICATION
    msg['Reply-To'] = email.originEmail
    msg.set_content(email.message)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_APPLICATION, PASSWORD_APPLICATION )
            smtp.send_message(msg)
        return {"status": "Email sent successfully"}
    except Exception as e:
        return {"error": str(e)}



