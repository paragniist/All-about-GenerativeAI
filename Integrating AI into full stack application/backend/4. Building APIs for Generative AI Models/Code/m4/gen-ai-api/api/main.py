import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from openai_bl import TextGenerationRequest, TextGenerationResponse, generate_text_openai
from openai_bl import ImageGenerationRequest, ImageGenerationResponse, generate_image_openai
from stablediffusion_bl import ImageCreationRequest, ImageCreationResponse, create_image_sd


app = FastAPI()


@app.post("/generate-text", response_model=TextGenerationResponse)
def generate_text(request: TextGenerationRequest):
    """
    Endpoint to generate text using OpenAI's API.

    Args:
        request (TextGenerationRequest): The request object containing the prompt and other parameters.

    Returns:
        TextGenerationResponse: The generated text response.
    """
    return generate_text_openai(request)


@app.post("/create-image", response_model=ImageCreationResponse)
def create_image(request: ImageCreationRequest):
    """
    Endpoint to create an image using OpenAI's API.

    Args:
        request (ImageCreationRequest): The request object containing the prompt.

    Returns:
        JSONResponse: The generated image in base64 format or an error message.
    """  
    prompt = request.prompt

    if not prompt:
         return JSONResponse(content={"error": "Prompt is required"}, status_code=400)
    
    img_str = generate_image_openai(prompt)
    return JSONResponse(content={"image": img_str})


if __name__ == "__main__":
    """
    Main entry point of the application.
    """     
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)

    # # OpenAI API Text Generation Sample
    # request = TextGenerationRequest(prompt="Create a short explanation of what is a Gen AI API!", max_tokens=50)
    # response = generate_text_openai(request)
    # print(response.generated_text)

    # # OpenAI API Image Generation Sample
    # request = ImageGenerationRequest(prompt="A bald man in his mountain bike in Costa Rica")
    # response = generate_image_openai(request)
    # print(response.image_base64)
    

    # # Stable Diffusion API Image Creation Sample
    # request = ImageCreationRequest(prompt="A bald man in his mountain bike in Costa Rica")
    # response = create_image_sd(request.prompt)
    # print(response.image_base64)    

