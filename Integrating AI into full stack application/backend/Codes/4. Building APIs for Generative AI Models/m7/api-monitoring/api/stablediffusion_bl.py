import torch
from diffusers import StableDiffusionPipeline
from pydantic import BaseModel
import base64
from io import BytesIO

class ImageCreationRequest(BaseModel):
    prompt: str

class ImageCreationResponse(BaseModel):
    image_url: str
    image_base64: str


# Check if GPU is available for faster generation
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Stable Diffusion model from Hugging Face
model_id = "CompVis/stable-diffusion-v1-4"  # You can also try other versions
pipeline = StableDiffusionPipeline.from_pretrained(model_id)
pipeline = pipeline.to(device)

def create_image_sd(prompt):
    """
    Create an image using Stable Diffusion.

    Args:
        prompt (str): The prompt for generating the image.

    Returns:
        ImageCreationResponse: The generated image response.
    """
    with torch.no_grad():
        image = pipeline(prompt).images[0]

    # Save the image locally as output.png
    # image.save("output.png")        

    # Convert the image to base64
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    return img_str