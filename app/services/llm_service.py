import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def generate_reply(prompt):
    try:
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 150
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)

        result = response.json()

        # ✅ handle HF loading / error cases
        if isinstance(result, dict) and result.get("error"):
            print("HF Error:", result)
            return fallback_response()

        # ✅ extract text safely
        if isinstance(result, list) and len(result) > 0:
            text = result[0].get("generated_text", "")
            return clean_response(text)

        return fallback_response()

    except Exception as e:
        print("LLM error:", e)
        return fallback_response()


def clean_response(text):
    # remove prompt repetition
    if "Lead Details:" in text:
        parts = text.split("Lead Details:")
        return parts[-1].strip()

    return text.strip()


def fallback_response():
    return (
        "✅ Thanks for sharing your details!\n\n"
        "Our team will review your profile and contact you shortly to guide you further. 🚀"
    )
