import torch
from diffusers import StableDiffusionPipeline
import matplotlib.pyplot as plt

# Check if GPU is available for faster generation
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Stable Diffusion model from Hugging Face
model_id = "CompVis/stable-diffusion-v1-4"  # You can also try other versions
pipeline = StableDiffusionPipeline.from_pretrained(model_id)
pipeline = pipeline.to(device)

# Define the text prompt
prompt = "A bald 45 year old man, riding a Canyon mountain bike down the side of the mountains of Costa Rica."

# Generate the image
with torch.no_grad():
    image = pipeline(prompt).images[0]

# Save the generated image
image.save("generated_image.png")

# Display the image
plt.imshow(image)
plt.axis("off")
plt.show()
