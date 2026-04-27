import torch
from diffusers import StableDiffusionPipeline
from pydantic import BaseModel
import base64
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ImageCreationRequest(BaseModel):
    prompt: str

class ImageCreationResponse(BaseModel):
    image_url: str
    image_base64: str

# Check if GPU is available for faster generation
device = "cuda" if torch.cuda.is_available() else "cpu"
logging.info(f"Using device: {device}")

# Load the Stable Diffusion model from Hugging Face
try:
    model_id = "CompVis/stable-diffusion-v1-4"  # You can also try other versions
    logging.info(f"Loading Stable Diffusion model: {model_id}")
    pipeline = StableDiffusionPipeline.from_pretrained(model_id)
    pipeline = pipeline.to(device)
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Failed to load Stable Diffusion model: {e}")
    raise

def create_image_sd(prompt):
    """
    Create an image using Stable Diffusion.

    Args:
        prompt (str): The prompt for generating the image.

    Returns:
        ImageCreationResponse: The generated image response.
    """
    logging.info(f"Received image creation request with prompt: {prompt}")
    try:
        with torch.no_grad():
            logging.info("Generating image...")
            image = pipeline(prompt).images[0]
            logging.info("Image generation successful.")

        # Convert the image to base64
        logging.info("Converting image to base64 format.")
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        logging.info("Image conversion to base64 completed.")

        return img_str
    except Exception as e:
        logging.error(f"Image creation failed for prompt: {prompt}. Error: {e}")
        raise
