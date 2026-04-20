import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from openai_bl import TextGenerationRequest, TextGenerationResponse, generate_text_openai
from openai_bl import ImageGenerationRequest, ImageGenerationResponse, generate_image_openai

from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log", mode="a", encoding="utf-8")
    ]
)

# Email configuration loaded from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))  # Default to 587 for TLS
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ALERT_RECEIVER = os.getenv("ALERT_RECEIVER")

def send_email_alert(subject: str, message: str):
    """Send an email alert."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = ALERT_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email alert: {e}")

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
    # Send an email alert when this endpoint is called
    send_email_alert(
        subject="Alert: /generate-text Endpoint Called",
        message=f"The /generate-text endpoint was called with prompt: {request.prompt}"
    )
    return generate_text_openai(request)



if __name__ == "__main__":
    """
    Main entry point of the application.
    """     
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
