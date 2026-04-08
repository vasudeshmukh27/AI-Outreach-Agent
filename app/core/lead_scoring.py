# Simple rule-based scoring

def score_lead(data):
    score = 0

    # Budget scoring
    budget = data.get("budget", "").lower()
    if "10" in budget or "15" in budget or "20" in budget:
        score += 40
    elif "5" in budget:
        score += 20

    # City scoring
    city = data.get("city", "").lower()
    tier1 = ["hyderabad", "mumbai", "bangalore", "delhi"]
    if city in tier1:
        score += 30
    else:
        score += 15

    # Timeline scoring
    timeline = data.get("timeline", "").lower()
    if "1" in timeline or "2" in timeline:
        score += 30
    else:
        score += 10

    if score >= 80:
        priority = "HIGH"
    elif score >= 50:
        priority = "MEDIUM"
    else:
        priority = "LOW"

    return score, priority