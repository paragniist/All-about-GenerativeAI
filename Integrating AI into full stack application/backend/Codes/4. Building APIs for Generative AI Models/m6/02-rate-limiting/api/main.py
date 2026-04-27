from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import uvicorn

# Initialize the Limiter with default InMemoryStorage
limiter = Limiter(key_func=get_remote_address)

# Initialize the FastAPI app
app = FastAPI()

# Middleware to handle rate limiting
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    try:
        # No need to call limiter.limit(request) explicitly
        response = await call_next(request)
        return response
    except RateLimitExceeded:
        return JSONResponse(
            status_code=429, content={"detail": "Rate limit exceeded"}
        )

# Exception handler for rate limiting
@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429, content={"detail": "Rate limit exceeded"}
    )

# Example route with rate limiting
@app.get("/limited")
@limiter.limit("5/minute")  # Limit to 5 requests per minute per IP
async def limited_endpoint(request: Request):  # Explicitly include "request"
    return {"message": "This route is rate-limited to 5 requests per minute."}

# Another route with a different rate limit
@app.get("/custom-limited")
@limiter.limit("2/minute")  # Limit to 2 requests per minute per IP
async def custom_limited_endpoint(request: Request):  # Explicitly include "request"
    return {"message": "This route is rate-limited to 2 requests per minute."}

# Route with no rate limit
@app.get("/no-limit")
async def no_limit_endpoint():
    return {"message": "This route has no rate limit."}

# Start the Uvicorn server when the script is run directly
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
