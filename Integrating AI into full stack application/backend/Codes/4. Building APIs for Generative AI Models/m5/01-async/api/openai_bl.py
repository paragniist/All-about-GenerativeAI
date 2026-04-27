import os
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



def generate_text_openai(request: TextGenerationRequest) -> TextGenerationResponse:
    """
    Generate text using OpenAI's API.

    Args:
        request (TextGenerationRequest): The request object containing the prompt and other parameters.

    Returns:
        TextGenerationResponse: The generated text response.
    """    
    return generate_chat_response(prompt=request.prompt, max_tokens=request.max_tokens)


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


 
async def generate_text_openai_async(request: TextGenerationRequest) -> TextGenerationResponse:
    """
    Generate text using OpenAI's API.

    Args:
        request (TextGenerationRequest): The request object containing the prompt and other parameters.

    Returns:
        TextGenerationResponse: The generated text response.
    """ 
    return await generate_chat_response_async(prompt=request.prompt, max_tokens=request.max_tokens)


async def generate_chat_response_async(
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

