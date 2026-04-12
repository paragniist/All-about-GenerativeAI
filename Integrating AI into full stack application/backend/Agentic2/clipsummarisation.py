from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Step 1: Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")

def summarize_text(text):

    # Step 2: Tokenize the input text
    inputs = tokenizer.encode(
        "summarize: " + text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    # Step 3: Generate summary
    outputs = model.generate(
        inputs,
        max_length=40,
        min_length=10,
        length_penalty=2.0,
        num_beams=5,
        early_stopping=True
    )

    # Step 4: Decode summary
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return summary


# Test the function
text = """
Artificial Intelligence is transforming industries such as healthcare,
finance, education, and transportation by automating complex tasks
and enabling data-driven decision making.
"""

print("Summary:")
print(summarize_text(text))