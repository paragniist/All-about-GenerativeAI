import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from pythonjsonlogger import jsonlogger

from openai_bl import TextGenerationRequest, TextGenerationResponse, generate_text_openai
# from openai_bl import ImageGenerationRequest, ImageGenerationResponse, generate_image_openai
# from stablediffusion_bl import ImageCreationRequest, ImageCreationResponse, create_image_sd

# Configure the logger to log to both console and a JSON lines file
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Create JSON formatter
json_formatter = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(message)s")

# File handler for JSON logs
file_handler = logging.FileHandler("app.jsonl", mode="a", encoding="utf-8")
file_handler.setFormatter(json_formatter)

# Stream handler for console
console_handler = logging.StreamHandler()
console_handler.setFormatter(json_formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

app = FastAPI()

# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info({"event": "request_received", "method": request.method, "url": str(request.url)})
    try:
        response = await call_next(request)
        logger.info({"event": "response_sent", "status_code": response.status_code, "url": str(request.url)})
        return response
    except Exception as e:
        logger.error({"event": "error", "url": str(request.url), "error": str(e)})
        raise e


@app.post("/generate-text", response_model=TextGenerationResponse)
def generate_text(request: TextGenerationRequest):
    """
    Endpoint to generate text using OpenAI's API.

    Args:
        request (TextGenerationRequest): The request object containing the prompt and other parameters.

    Returns:
        TextGenerationResponse: The generated text response.
    """
    logger.info({"event": "text_generation", "prompt": request.prompt})
    try:
        response = generate_text_openai(request)
        logger.info({"event": "text_generation_completed", "prompt": request.prompt})
        return response
    except Exception as e:
        logger.error({"event": "text_generation_failed", "prompt": request.prompt, "error": str(e)})
        return JSONResponse(
            content={"error": "Failed to generate text.", "details": str(e)},
            status_code=500,
        )


if __name__ == "__main__":
    """
    Main entry point of the application.
    """
    logger.info({"event": "server_starting"})
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
