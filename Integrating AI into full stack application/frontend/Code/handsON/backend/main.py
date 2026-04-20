import os
import time
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from textblob import TextBlob
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
from models import Base, ChatLog

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Chat with Telemetry")

# -------------------------
# DATABASE STARTUP
# -------------------------

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting application...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")


# -------------------------
# REQUEST / RESPONSE MODELS
# -------------------------

class ChatRequest(BaseModel):
    prompt: str
    user_id: str


class ChatResponse(BaseModel):
    response: str
    tokens_used: int
    sentiment: dict
    response_time_ms: int


# -------------------------
# OPENAI CALL
# -------------------------
client = OpenAI(api_key="")


def call_openai(prompt: str):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "response": response.choices[0].message.content,
        "tokens": {
            "total_tokens": response.usage.total_tokens
        }
    }

# -------------------------
# SENTIMENT ANALYSIS
# -------------------------

def analyze_sentiment(text: str):

    blob = TextBlob(text)

    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity > 0.2:
        desc = "positive"
    elif polarity < -0.2:
        desc = "negative"
    else:
        desc = "neutral"

    return {
        "polarity": polarity,
        "subjectivity": subjectivity,
        "description": desc
    }


# -------------------------
# DATABASE LOGGING
# -------------------------

def save_chat_log(user_id, prompt, response, tokens, sentiment, db: Session):

    chat = ChatLog(
        user_id=user_id,
        prompt=prompt,
        response=response,
        tokens=tokens,
        sentiment=sentiment
    )

    db.add(chat)
    db.commit()


# -------------------------
# CHAT ENDPOINT
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest, db: Session = Depends(get_db)):

    start_time = time.time()

    try:

        openai_result = call_openai(request.prompt)
        ai_response = openai_result["response"]
        tokens = openai_result["tokens"]

        sentiment = analyze_sentiment(ai_response)

        response_time = int((time.time() - start_time) * 1000)

        save_chat_log(
            user_id=request.user_id,
            prompt=request.prompt,
            response=ai_response,
            tokens=tokens["total_tokens"],
            sentiment=sentiment["polarity"],
            db=db
        )

        return ChatResponse(
            response=ai_response,
            tokens_used=tokens["total_tokens"],
            sentiment=sentiment,
            response_time_ms=response_time
        )

    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="AI processing failed")