from app.core.funnel import get_next_question, get_next_stage
from app.core.lead_scoring import score_lead

# In-memory storage (later replace with DB)
user_states = {}
user_data = {}

def handle_message(user_id, message):
    # initialize user
    if user_id not in user_states:
        user_states[user_id] = "NEW"
        user_data[user_id] = {}

    stage = user_states[user_id]

    # store answers
    if stage == "BUDGET":
        user_data[user_id]["budget"] = message
    elif stage == "CITY":
        user_data[user_id]["city"] = message
    elif stage == "TIMELINE":
        user_data[user_id]["timeline"] = message

    # move to next stage
    next_stage = get_next_stage(stage)
    user_states[user_id] = next_stage

    # if done → score lead
    if next_stage == "DONE":
        data = user_data[user_id]
        score, priority = score_lead(data)

        return (
            f"✅ Lead Analysis Complete\n\n"
            f"Budget: {data.get('budget')}\n"
            f"City: {data.get('city')}\n"
            f"Timeline: {data.get('timeline')}\n\n"
            f"Score: {score}\n"
            f"Priority: {priority}\n\n"
            f"Our team will contact you soon!"
        )

    # ask next question
    return get_next_question(next_stage)