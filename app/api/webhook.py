from fastapi import APIRouter, Request
from app.services.telegram_service import send_message

router = APIRouter()

@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    try:
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        print(f"User: {message}")

        reply = f"You said: {message}"

        send_message(chat_id, reply)

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}