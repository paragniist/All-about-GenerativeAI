from fastapi import FastAPI
from pydantic import BaseModel
from sentiment_agent import analyze_sentiment

app = FastAPI()

class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Sentiment AI Agent is running"}


@app.post("/analyze")
def analyze(request: TextRequest):

    sentiment = analyze_sentiment(request.text)

    return {
        "input_text": request.text,
        "sentiment": sentiment
    }