import requests
import random
import time
import os
import json


API_URL = "http://127.0.0.1:8000/generate-text-cache" # add -cache to the end of the URL to use the cache


def load_prompts_from_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data['prompts']


def pick_random_prompts(prompts, count):
    return random.sample(prompts, count)


def ensure_n_prompts(prompts, n):
    if len(prompts) >= n:
        return random.sample(prompts, n)
    else:
        repeated_prompts = (prompts * (n // len(prompts) + 1))[:n]
        return random.sample(repeated_prompts, n)


def generate_text(prompt):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 100
    }
        
    response = requests.post(API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":   
    prompts = load_prompts_from_json('./prompts.json')
    n = 5
    prompts_n = ensure_n_prompts(prompts, n)

    start_time = time.time()
    for prompt in prompts_n:
        generate_text(prompt) # prompt
    elapsed_time_ms = (time.time() - start_time) * 1000   
    print(f"Time taken: {elapsed_time_ms:.2f} ms")