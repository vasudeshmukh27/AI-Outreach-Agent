import re

def extract_info(message):
    data = {}

    # Budget
    budget_match = re.search(r'(\d+)\s*(lakh|lakhs|l)', message.lower())
    if budget_match:
        data["budget"] = budget_match.group()

    # City (simple detection)
    cities = ["hyderabad", "mumbai", "bangalore", "delhi"]
    for city in cities:
        if city in message.lower():
            data["city"] = city

    # Timeline
    timeline_match = re.search(r'(\d+)\s*(month|months)', message.lower())
    if timeline_match:
        data["timeline"] = timeline_match.group()

    return data