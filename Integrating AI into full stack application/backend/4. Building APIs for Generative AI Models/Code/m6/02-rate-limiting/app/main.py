import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def call_endpoint(endpoint):
    """
    Calls the specified endpoint and prints the result.
    """
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        if response.status_code == 200:
            print(f"SUCCESS: {endpoint} - {response.json()['message']}")
        elif response.status_code == 429:
            print(f"RATE LIMIT EXCEEDED: {endpoint} - {response.json()['detail']}")
        else:
            print(f"ERROR: {endpoint} - {response.status_code}, {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"EXCEPTION: {e}")

def main():
    """
    Calls the /limited and /no-limit endpoints multiple times.
    """
    print("Starting API calls to demonstrate rate limiting...\n")

    for i in range(10):  # Adjust the range to test more or fewer requests
        print(f"Attempt {i + 1}...")
        call_endpoint("/custom-limited")  # Call the custom limited endpoint
        call_endpoint("/limited")  # Call the limited endpoint
        call_endpoint("/no-limit")  # Call the non-limited endpoint
        time.sleep(1)  # Wait 5 seconds between calls to simulate normal usage

if __name__ == "__main__":
    main()
