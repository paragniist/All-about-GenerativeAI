import random
import json
import asyncio
import httpx
import os
import time

API_URL = "http://127.0.0.1:8000/generate-text"
TIMEOUT = 60  # Timeout in seconds

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

async def make_api_call(client, prompt):
    try:
        response = await client.post(API_URL, json={"prompt": prompt, "max_tokens": 1000})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code} for prompt: {prompt}")
            return None
    except httpx.ReadTimeout:
        print(f"Request timed out for prompt: {prompt}")
        return None

async def call_generate_text_in_batches(prompts, batch_size):
    print(f"Prompts: {prompts}")
    print(f"Batch size: {batch_size}")
    print(f"API URL: {API_URL}")
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        responses = []
        for i in range(0, len(prompts), batch_size):
            print(f"Processing batch starting at index {i}")
            batch = prompts[i:i + batch_size]
            print(f"Batch: {batch}")
            tasks = [make_api_call(client, prompt) for prompt in batch]
            batch_responses = await asyncio.gather(*tasks)
            responses.extend([response for response in batch_responses if response is not None])
        return responses

if __name__ == "__main__":   
    try:
        prompts = load_prompts_from_json('./prompts.json')
        print(f"Loaded prompts: {prompts}")
        n = 6
        prompts_n = ensure_n_prompts(prompts, n)
        print(f"Ensured {n} prompts: {prompts_n}")
        batch_size = 3

        start_time = time.time()
        responses = asyncio.run(call_generate_text_in_batches(prompts_n, batch_size))
        end_time = time.time()
        
        elapsed_time_ms = (end_time - start_time) * 1000
        print(f"Responses: {responses}")
        print(f"Time taken: {elapsed_time_ms:.2f} ms")
   
    except FileNotFoundError as e:
        print(e)