import os
import base64
import requests
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

# Load environment variables from a .env file
load_dotenv()
key = os.getenv("OPENAI_API_KEY")

# Create the client with the OpenAI API key
client = OpenAI(api_key=key)


class TextGenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 1000

class TextGenerationResponse(BaseModel):
    generated_text: str

class ImageGenerationRequest(BaseModel):
    prompt: str

class ImageGenerationResponse(BaseModel):
    image_url: str
    image_base64: str


def generate_text_openai(request: TextGenerationRequest) -> TextGenerationResponse:
    """
    Generate text using OpenAI's API.

    Args:
        request (TextGenerationRequest): The request object containing the prompt and other parameters.

    Returns:
        TextGenerationResponse: The generated text response.
    """    
    return generate_chat_response(prompt=request.prompt, max_tokens=request.max_tokens)


def generate_image_openai(request: ImageGenerationRequest) -> ImageGenerationResponse:
    """
    Generate an image using OpenAI's API.

    Args:
        request (ImageGenerationRequest): The request object containing the prompt.

    Returns:
        ImageGenerationResponse: The generated image response.
    """    
    return generate_image_response(image_prompt=request.prompt)


def generate_chat_response(
    prompt: str,
    system_message: str = "You are a helpful assistant.",
    model: str = "gpt-3.5-turbo",
    max_tokens: int = 150,
) -> str:
    """
    Generate a chat response using OpenAI's API.

    Args:
        prompt (str): The prompt for generating the chat response.
        system_message (str): The system message for the chat model.
        model (str): The model to use for generating the response.
        max_tokens (int): The maximum number of tokens for the response.

    Returns:
        str: The generated chat response.
    """
    # Call the OpenAI Chat Completions API
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=max_tokens
    )

    # Extract the generated content
    generated_response = response.choices[0].message.content
    return TextGenerationResponse(generated_text=generated_response) 



def generate_image_response(
    image_prompt: str
) -> str:
    """
    Generate an image response using OpenAI's API, with DALL-E.

    Args:
        image_prompt (str): The prompt for generating the image.

    Returns:
        ImageGenerationResponse: The generated image response.
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        url = response.data[0].url

                # Fetch the image from the URL
        image_response = requests.get(url)
        image_response.raise_for_status()  # Check if the request was successful
        
        # Convert the image content to base64
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')

        # Save the base64 image locally
        # with open("generated_image.png", "wb") as image_file:
        #     image_file.write(base64.b64decode(image_base64))
        
        return ImageGenerationResponse(image_url=url, image_base64=image_base64)

    except Exception as e:
        print(f"Error: {e}")