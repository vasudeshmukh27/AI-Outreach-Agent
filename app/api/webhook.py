from fastapi import APIRouter, Request
from app.services.telegram_service import send_message
from app.core.conversation import handle_message
from app.core.followup_checker import check_and_send_followups

router = APIRouter()


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request):
    data = await request.json()

    try:
        # Extract message safely
        if "message" not in data:
            return {"status": "ignored"}

        message_data = data["message"]

        # Handle non-text messages safely
        if "text" not in message_data:
            return {"status": "no text"}

        message = message_data["text"]
        chat_id = message_data["chat"]["id"]

        print(f"User ({chat_id}): {message}")

        # 🔥 1. Run follow-up checker (FREE alternative to cron)
        check_and_send_followups()

        # 🧠 2. Process user message
        reply = handle_message(chat_id, message)

        # 📤 3. Send reply
        send_message(chat_id, reply)

    except Exception as e:
        print("Error in webhook:", e)

    return {"status": "ok"}