import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

model.to(device)

def analyze_sentiment(text):

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=128
    ).to(device)

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=-1)

    sentiment = "Positive" if torch.argmax(probabilities) == 1 else "Negative"

    return sentiment