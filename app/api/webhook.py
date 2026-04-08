from fastapi import APIRouter, Request
from app.services.telegram_service import send_message
from app.core.conversation import handle_message

router = APIRouter()

@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    try:
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        print(f"User ({chat_id}): {message}")

        reply = handle_message(chat_id, message)

        send_message(chat_id, reply)

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}