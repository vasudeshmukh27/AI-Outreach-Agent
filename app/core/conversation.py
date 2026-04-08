from app.core.lead_scoring import score_lead
from app.core.extractor import extract_info
from app.services.llm_service import generate_reply
from app.services.supabase_service import (
    get_user,
    create_user,
    get_lead,
    upsert_lead,
    save_score,
    update_last_message
)


def handle_message(user_id, message):
    # ✅ Ensure user exists
    if not get_user(user_id):
        create_user(user_id)

    # ✅ Get existing lead data
    existing = get_lead(user_id)
    data = existing[0] if existing else {}

    # 🔍 Extract info from user message
    extracted = extract_info(message)
    data.update(extracted)

    # ✅ Save updated lead info
    upsert_lead(user_id, data)

    # ✅ Update last interaction time (IMPORTANT for follow-ups)
    update_last_message(user_id)

    # 🧠 Ask for missing fields (dynamic flow)
    if not data.get("budget"):
        return "💰 What is your budget range for starting the franchise?"

    if not data.get("city"):
        return "📍 Which city are you planning to start in?"

    if not data.get("timeline"):
        return "⏳ What is your expected timeline to start?"

    # ✅ All data collected → score lead
    score, priority = score_lead(data)
    save_score(user_id, score, priority)

    # 🤖 Generate AI response (sales-style)
    prompt = f"""
    You are a professional franchise sales consultant.

    Lead Details:
    Budget: {data.get('budget')}
    City: {data.get('city')}
    Timeline: {data.get('timeline')}

    Lead Score: {score}
    Priority: {priority}

    Write a persuasive, friendly response encouraging the user to book a call.
    Keep it concise and human-like.
    """

    return generate_reply(prompt)