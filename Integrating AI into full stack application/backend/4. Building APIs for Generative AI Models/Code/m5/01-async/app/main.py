import time
import requests
import asyncio
import aiohttp

API_URL = "http://127.0.0.1:8000/generate-text"

prompts = [
    "Explain the concept of a neural network in simple terms.",
    "Describe the differences between supervised and unsupervised learning.",
    "What are the key components of a generative adversarial network (GAN)?",
    "How does transfer learning improve the performance of AI models?",
    "What are the ethical considerations when using generative AI in content creation?"
]

def generate_text():
    start_time = time.time()
    for prompt in prompts:
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
            print("Response:", response.json())
        else:
            print("Error:", response.status_code, response.text)

    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000
    return elapsed_time_ms


async def generate_text_async():
    start_time = time.time()    
    # Create a list of tasks for asynchronous execution
    tasks = [make_request(prompt) for prompt in prompts]
    
    # Gather and execute all tasks concurrently
    await asyncio.gather(*tasks)

    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000
    return elapsed_time_ms

async def make_request(prompt):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json={"prompt": prompt}) as response:
            if response.status == 200:
                result = await response.json()
                print(f"Prompt: {prompt}\nResponse: {result['generated_text']}\n")
            else:
                print(f"Failed to get response for prompt: {prompt}. Status code: {response.status}")


if __name__ == "__main__":
    sync_time = generate_text()
    async_time = asyncio.run(generate_text_async())

    print("Synchronous execution time:", sync_time, "ms")
    print("Asynchronous execution time:", async_time, "ms")
    
    improvement_percent = ((sync_time - async_time) / sync_time) * 100
    print(f"Asynchronous execution was {improvement_percent:.2f}% faster")