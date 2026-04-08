# Handles user stages

def get_next_question(stage):
    flow = {
        "NEW": "Welcome! Interested in starting a franchise?",
        "BUDGET": "What is your budget range?",
        "CITY": "Which city are you planning to start in?",
        "TIMELINE": "What is your expected timeline to start?",
        "DONE": "Thanks! Analyzing your profile..."
    }
    return flow.get(stage, "Let's continue.")

def get_next_stage(current_stage):
    stages = ["NEW", "BUDGET", "CITY", "TIMELINE", "DONE"]
    try:
        idx = stages.index(current_stage)
        return stages[idx + 1]
    except:
        return "DONE"