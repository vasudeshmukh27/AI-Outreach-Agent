from datetime import datetime, timedelta
from app.services.supabase_service import (
    get_pending_followups,
    mark_followup_sent
)
from app.services.telegram_service import send_message

FOLLOWUP_DELAY_MINUTES = 5  # for testing (later change to 60 or 1440)


def run_followups():
    leads = get_pending_followups()

    for lead in leads:
        chat_id = lead.get("chat_id")
        last_time = lead.get("last_message_at")
        followup_sent = lead.get("followup_sent")

        if not chat_id or not last_time or followup_sent:
            continue

        # Convert time
        last_time = datetime.fromisoformat(last_time.replace("Z", "+00:00"))
        now = datetime.utcnow()

        diff = now - last_time

        # ⏱️ Check delay
        if diff > timedelta(minutes=FOLLOWUP_DELAY_MINUTES):
            print(f"Sending follow-up to {chat_id}")

            send_message(
                chat_id,
                "Hey! Just checking — are you still interested in starting a franchise? 😊"
            )

            mark_followup_sent(chat_id)


if __name__ == "__main__":
    run_followups()