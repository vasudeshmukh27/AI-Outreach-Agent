from fastapi import FastAPI
from app.api import webhook

app = FastAPI()

app.include_router(webhook.router)

@app.get("/")
def root():
    return {"message": "AI Outreach Agent Running "}