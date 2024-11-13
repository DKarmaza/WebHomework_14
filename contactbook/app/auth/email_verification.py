from fastapi_mail import FastMail, MassageSchema, ConectionConfig
from fastapi import BackgroundTasks
from .schemas import User
import os

conf = ConectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

async def send_verification_email(email: str, token: str, BackgroundTasks: BackgroundTasks):
    massage = MassageSchema(
        subject="Verify your email",
        recipients=[email],
        body=f"Please verify your email by cliking that link: http://localhost:8000/verify-email?token={token}",
        subtype="html"
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, massage)