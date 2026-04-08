import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

def generate_reply(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    try:
        return result[0]["generated_text"]
    except:
        return "Sorry, something went wrong."