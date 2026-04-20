def choose_model(prompt:dict)-> str:
    text = prompt["text"]
    tone = prompt["tone"]

    if "playful" in tone.lower() and len(text) < 200:
        return "gpt-4"
    elif "summary" in tone.lower():
        return "mockAImodel"
    else:
        return "gemini-2.0-flash"