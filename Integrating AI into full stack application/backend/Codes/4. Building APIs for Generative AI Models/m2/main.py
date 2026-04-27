from fastapi import FastAPI 
from pydantic import BaseModel
import uvicorn


app = FastAPI()

class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 1000

class TextGenerationResponse(BaseModel):
    generated_text: str

@app.post("/generate-text", response_model=TextGenerationResponse)
def generate_text(request: TextGenerationRequest):
    return TextGenerationResponse(generated_text="Text generated: " + request.prompt)      


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)

