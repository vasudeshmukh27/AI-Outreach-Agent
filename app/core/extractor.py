import re

def extract_info(message):
    data = {}
    msg = message.lower()

    # 💰 Budget (handles lakh + raw numbers)
    budget_match = re.search(r'(\d+)\s*(lakh|lakhs|l)', msg)
    if budget_match:
        data["budget"] = budget_match.group()
    else:
        # ✅ NEW: detect raw numbers like 1000000
        number_match = re.search(r'\b\d{5,}\b', msg)
        if number_match:
            data["budget"] = number_match.group()

    # 📍 City
    cities = ["hyderabad", "mumbai", "bangalore", "delhi"]
    for city in cities:
        if city in msg:
            data["city"] = city

    # ⏳ Timeline
    timeline_match = re.search(r'(\d+)\s*(month|months)', msg)
    if timeline_match:
        data["timeline"] = timeline_match.group()

    return data
