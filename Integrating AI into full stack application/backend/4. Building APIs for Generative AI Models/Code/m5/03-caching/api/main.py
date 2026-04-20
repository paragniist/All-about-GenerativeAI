from fastapi import FastAPI
from functools import lru_cache
from openai_bl import TextGenerationRequest, TextGenerationResponse, generate_text_openai
import uvicorn

app = FastAPI()

# Simple LRU cache for the generate_text_openai function
@lru_cache(maxsize=128)
def cached_generate_text(prompt: str, max_tokens: int) -> TextGenerationResponse:
    request = TextGenerationRequest(prompt=prompt, max_tokens=max_tokens)
    return generate_text_openai(request)


@app.post("/generate-text-cache", response_model=TextGenerationResponse)
def generate_text_cache(request: TextGenerationRequest):
    print(f"Processing request for prompt: {request.prompt}")
    return cached_generate_text(request.prompt, request.max_tokens)


@app.post("/generate-text", response_model=TextGenerationResponse)
def generate_text_cache(request: TextGenerationRequest):
    print(f"Processing non cached request for prompt: {request.prompt}")
    return generate_text_openai(request)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
