import requests
from django.core.mail import send_mail
from django.conf import settings

TELEGRAM_TOKEN = "BOT_TOKEN"  # bu keyin .env dan olinadi
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

def send_telegram_message(chat_id, text):
    data = {"chat_id": chat_id, "text": text}
    requests.post(TELEGRAM_API, data=data)

def send_email_notification(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=True
    )
