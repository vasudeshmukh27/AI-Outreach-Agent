from app.services.supabase_service import supabase

def get_faq_answer(message):
    response = supabase.table("faqs").select("*").execute()
    faqs = response.data

    for faq in faqs:
        if faq["question"].lower() in message.lower():
            return faq["answer"]

    return None