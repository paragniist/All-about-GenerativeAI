import requests

def generate_text():
    prompt = "Create a short explanation of the concept of a neural network."
    url = "http://127.0.0.1:8000/generate-text"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 1000
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Response:", response.json())
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    generate_text()
