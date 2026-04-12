import os
import openai
from google import generativeai as genai
import dotenv

dotenv.load_dotenv()

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GENAI_API_KEY"))

def call_openai_gpt4(data):
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": data["text"]}]
    )
    return response.choices[0].message.content

def call_gemini(data):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(data["text"])
    print(response)
    return response.text

def call_mock_api(data):
    return "[Stub] mockAIModel model response for: " + data["text"]

model_strategies = {
    "gpt-4": call_openai_gpt4,
    "gemini-2.0-flash": call_gemini,
    "mockAIModel": call_mock_api
}