import requests

url = "http://localhost:8000/generate"

json_data = {
    "prompt": "hello, How are you ?"
}

try:
    response = requests.post(url, json=json_data)

    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
