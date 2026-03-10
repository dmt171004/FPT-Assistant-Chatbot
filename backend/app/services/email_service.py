from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import (
    MAIL_USERNAME,
    MAIL_PASSWORD,
    MAIL_FROM,
    MAIL_PORT,
    MAIL_SERVER,
)

conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=True,     
    MAIL_SSL_TLS=False,     
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


# =========================
# RESET PASSWORD EMAIL
# =========================
async def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8080/reset-password?token={token}"

    message = MessageSchema(
        subject="Password Reset",
        recipients=[email],
        body=f"""
Click the link below to reset your password:

{reset_link}

This link will expire in 10 minutes.
""",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)


# =========================
# EMAIL VERIFICATION
# =========================
async def send_verification_email(email: str, token: str):

    verification_link = f"http://localhost:8080/verify-email?token={token}"

    print("Sending verification email to:", email)
    print("Verification link:", verification_link)

    message = MessageSchema(
        subject="Verify your account",
        recipients=[email],
        body=f"""
Hello,

Thank you for registering an account.

Verify your email by opening the link below:

{verification_link}

The link will expire in 24 hours.

If you did not create this account, you can ignore this email.
""",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    print("Verification email sent!")