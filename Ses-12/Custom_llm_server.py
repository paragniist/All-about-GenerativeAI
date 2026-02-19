from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(
 api_key=os.getenv("GEMINI_KEY"),
 base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class RequestData(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_ai(data: RequestData):

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role":"system","content":"You are helpful"},
            {"role":"user","content":data.prompt}
        ]
    )

    return {
        "reply": response.choices[0].message.content
    }
