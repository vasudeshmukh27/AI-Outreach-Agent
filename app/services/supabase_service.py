from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_user(chat_id):
    response = supabase.table("users").select("*").eq("chat_id", chat_id).execute()
    return response.data


def create_user(chat_id):
    supabase.table("users").insert({"chat_id": chat_id}).execute()


def get_lead(chat_id):
    response = supabase.table("leads").select("*").eq("chat_id", chat_id).execute()
    return response.data


def upsert_lead(chat_id, data):
    supabase.table("leads").upsert(
        {
            "chat_id": chat_id,
            "budget": data.get("budget"),
            "city": data.get("city"),
            "timeline": data.get("timeline"),
        },
        on_conflict="chat_id"
    ).execute()
    

def save_score(chat_id, score, priority):
    supabase.table("leads").update({
        "score": score,
        "priority": priority
    }).eq("chat_id", chat_id).execute()


def update_last_message(chat_id):
    supabase.table("leads").update({
        "last_message_at": "now()",
        "followup_sent": False
    }).eq("chat_id", chat_id).execute()


def get_pending_followups():
    response = supabase.table("leads").select("*").execute()
    return response.data


def mark_followup_sent(chat_id):
    supabase.table("leads").update({
        "followup_sent": True
    }).eq("chat_id", chat_id).execute()
