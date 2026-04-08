from app.core.funnel import get_next_question, get_next_stage
from app.core.lead_scoring import score_lead
from app.core.extractor import extract_info
from app.services.llm_service import generate_reply

user_states = {}
user_data = {}

def handle_message(user_id, message):
    # Initialize
    if user_id not in user_states:
        user_states[user_id] = "NEW"
        user_data[user_id] = {}

    # 🔍 Extract info from message
    extracted = extract_info(message)
    user_data[user_id].update(extracted)

    data = user_data[user_id]

    # 🧠 Check what is missing
    if "budget" not in data:
        user_states[user_id] = "BUDGET"
        return get_next_question("BUDGET")

    if "city" not in data:
        user_states[user_id] = "CITY"
        return get_next_question("CITY")

    if "timeline" not in data:
        user_states[user_id] = "TIMELINE"
        return get_next_question("TIMELINE")

    # ✅ All data collected → score
    score, priority = score_lead(data)

    # 🤖 Generate smart reply using LLM
    prompt = f"""
    You are a franchise sales expert.

    Lead details:
    Budget: {data.get('budget')}
    City: {data.get('city')}
    Timeline: {data.get('timeline')}

    Score: {score}
    Priority: {priority}

    Generate a persuasive, professional response encouraging them to book a call.
    """

    ai_response = generate_reply(prompt)

    return ai_response