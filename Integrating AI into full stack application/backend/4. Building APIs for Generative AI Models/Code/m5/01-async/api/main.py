from fastapi import FastAPI 
import uvicorn
from openai_bl import TextGenerationRequest, TextGenerationResponse, generate_text_openai, generate_text_openai_async


app = FastAPI()


@app.post("/generate-text", response_model=TextGenerationResponse)
def generate_text(request: TextGenerationRequest):
    return generate_text_openai(request)


@app.post("/generate-text-async", response_model=TextGenerationResponse)
async def generate_text_async(request: TextGenerationRequest):
    return await generate_text_openai_async(request)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)

