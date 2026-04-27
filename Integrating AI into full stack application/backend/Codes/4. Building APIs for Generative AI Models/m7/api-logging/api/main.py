import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging

from openai_bl import TextGenerationRequest, TextGenerationResponse, generate_text_openai
# from openai_bl import ImageGenerationRequest, ImageGenerationResponse, generate_image_openai
# from stablediffusion_bl import ImageCreationRequest, ImageCreationResponse, create_image_sd

# Configure the logger to log to both console and a file
logging.basicConfig(
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Log to console
        logging.FileHandler("app.log", mode="a", encoding="utf-8"),  # Log to file
    ],
)

app = FastAPI()

# Middleware to log requests and responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logging.info(f"Response: {response.status_code} for {request.url}")
        return response
    except Exception as e:
        logging.error(f"Error: {e} at {request.url}")
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
    logging.info(f"Text generation request received with prompt: {request.prompt}")
    response = generate_text_openai(request)
    logging.info(f"Text generation completed for prompt: {request.prompt}")
    return response


# Uncomment and use this endpoint if needed
# @app.post("/create-image", response_model=ImageCreationResponse)
# def create_image(request: ImageCreationRequest):
#     """
#     Endpoint to create an image using OpenAI's API.

#     Args:
#         request (ImageCreationRequest): The request object containing the prompt.

#     Returns:
#         JSONResponse: The generated image in base64 format or an error message.
#     """
#     prompt = request.prompt

#     if not prompt:
#         logging.warning("Image generation request failed: Prompt is required")
#         return JSONResponse(content={"error": "Prompt is required"}, status_code=400)
    
#     logging.info(f"Image generation request received with prompt: {prompt}")
#     try:
#         img_str = generate_image_openai(prompt)
#         logging.info(f"Image generation completed for prompt: {prompt}")
#         return JSONResponse(content={"image": img_str})
#     except Exception as e:
#         logging.error(f"Image generation failed for prompt: {prompt}, error: {e}")
#         return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == "__main__":
    """
    Main entry point of the application.
    """
    logging.info("Starting FastAPI server...")
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
