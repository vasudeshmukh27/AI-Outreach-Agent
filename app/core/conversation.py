from app.core.lead_scoring import score_lead
from app.core.extractor import extract_info
from app.core.faq import get_faq_answer
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

    # 🔍 FAQ handling (FIRST priority)
    faq_answer = get_faq_answer(message)
    if faq_answer:
        return faq_answer

    # ✅ Get existing lead data
    existing = get_lead(user_id)
    data = existing[0] if existing else {}

    # 🔍 Extract structured info from message
    extracted = extract_info(message)
    data.update(extracted)

    # ✅ Save updated lead
    upsert_lead(user_id, data)

    # ✅ Update last interaction time (for follow-ups)
    update_last_message(user_id)

    # 🧠 Ask missing information dynamically
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

    Write a persuasive, friendly, human-like response encouraging the user to book a call.
    Keep it concise (3-4 lines max).
    """

    ai_response = generate_reply(prompt)

    return ai_response