from fastapi import FastAPI
import uvicorn
from uuid import uuid4
from typing import List
import asyncio
from openai_bl import TextGenerationRequest, TextGenerationResponse, generate_text_openai
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the batch processor in the background
    task = asyncio.create_task(batch_processor())
    yield
    task.cancel()
    await task


app = FastAPI(lifespan=lifespan)

# Shared queue and response map
request_queue = asyncio.Queue()  # Use asyncio.Queue for thread-safe operations
response_map = {}

# Batch processing interval and size
BATCH_INTERVAL = 0.5  # Process batches every 0.5 seconds
BATCH_SIZE = 5  # Maximum number of requests per batch


# Generate responses for a batch
async def generate_batch_responses(batch_requests: List[TextGenerationRequest]) -> List[TextGenerationResponse]:
    print(f"Generating responses for batch of size {len(batch_requests)}")
    responses = []
    for request in batch_requests:
        print(f"Generating response for prompt: {request.prompt}")
        response = await generate_text_openai(request)
        responses.append(response)
    return responses


# Background task to process batches
async def batch_processor():
    while True:
        batch = []
        # Collect a batch of requests
        while len(batch) < BATCH_SIZE:
            try:
                # Timeout to avoid waiting indefinitely
                item = await asyncio.wait_for(request_queue.get(), timeout=BATCH_INTERVAL)
                batch.append(item)
            except asyncio.TimeoutError:
                break

        if batch:
            # Extract IDs and corresponding requests
            ids, requests = zip(*batch)

            # Process the batch
            responses = await generate_batch_responses(list(requests))

            # Map responses to their corresponding IDs
            for id, response in zip(ids, responses):
                response_map[id] = response
                print(f"Response for ID {id} added to response_map")


@app.post("/generate-text", response_model=TextGenerationResponse)
async def generate_text(request: TextGenerationRequest):
    print(f"Received request to generate text for prompt: {request.prompt}")

    # Generate a unique ID for the request
    request_id = str(uuid4())

    # Add the request to the queue
    await request_queue.put((request_id, request))
    print(f"Request ID {request_id} added to queue")

    # Wait for the response
    while request_id not in response_map:
        print(f"Waiting for response for request ID: {request_id}")
        await asyncio.sleep(0.1)

    # Retrieve and remove the response from the map
    response = response_map.pop(request_id)
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)
