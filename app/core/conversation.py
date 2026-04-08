from app.core.lead_scoring import score_lead
from app.core.extractor import extract_info
from app.services.llm_service import generate_reply
from app.services.supabase_service import (
    get_user, create_user, get_lead, upsert_lead, save_score
)


def handle_message(user_id, message):
    # ✅ Ensure user exists
    if not get_user(user_id):
        create_user(user_id)

    # ✅ Get existing lead data
    existing = get_lead(user_id)
    data = existing[0] if existing else {}

    # 🔍 Extract new info
    extracted = extract_info(message)
    data.update(extracted)

    # ✅ Save updated lead
    upsert_lead(user_id, data)

    # 🧠 Ask missing info
    if not data.get("budget"):
        return "What is your budget range?"

    if not data.get("city"):
        return "Which city are you planning to start in?"

    if not data.get("timeline"):
        return "What is your expected timeline?"

    # ✅ Score lead
    score, priority = score_lead(data)
    save_score(user_id, score, priority)

    # 🤖 AI response
    prompt = f"""
    You are a franchise sales expert.

    Lead details:
    Budget: {data.get('budget')}
    City: {data.get('city')}
    Timeline: {data.get('timeline')}

    Score: {score}
    Priority: {priority}

    Respond professionally and encourage booking a call.
    """

    return generate_reply(prompt)