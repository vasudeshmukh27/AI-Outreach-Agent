import requests
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def send_message(chat_id: int, text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": text
    }

    response = requests.post(url, json=payload)
    return response.json()