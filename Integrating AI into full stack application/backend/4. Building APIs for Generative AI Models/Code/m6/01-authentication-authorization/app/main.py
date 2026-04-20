import requests

BASE_URL = "http://127.0.0.1:8000"

def login(username, password):
    """
    Logs in with the given username and password to obtain a JWT token.
    """
    url = f"{BASE_URL}/token"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    
    if response.status_code == 200:
        token = response.json().get("access_token")
        print(f"Login successful for {username}. Token: {token}")
        return token
    else:
        print(f"Login failed for {username}: {response.json()}")
        return None

def access_protected_route(endpoint, token):
    """
    Access a protected route using the given token.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print(f"Accessed {endpoint} successfully: {response.json()}")
    else:
        print(f"Failed to access {endpoint}: {response.status_code}, {response.json()}")

if __name__ == "__main__":
    # Test login with valid and invalid credentials
    print("Testing login...")
    user_token = login("john", "password123")  # Valid credentials
    admin_token = login("admin", "admin123")  # Valid credentials
    invalid_token = login("invalid", "wrongpassword")  # Invalid credentials

    # Test protected routes with valid tokens
    if user_token:
        print("\nTesting user-only route with user token...")
        access_protected_route("/user-only", user_token)

        print("\nTesting admin-only route with user token...")
        access_protected_route("/admin-only", user_token)  # Should fail

    if admin_token:
        print("\nTesting admin-only route with admin token...")
        access_protected_route("/admin-only", admin_token)

        print("\nTesting user-only route with admin token...")
        access_protected_route("/user-only", admin_token)  # Should succeed

    # Test protected routes with invalid token
    if invalid_token:
        print("\nTesting user-only route with invalid token...")
        access_protected_route("/user-only", invalid_token)

    print("\nTesting protected route without token...")
    access_protected_route("/user-only", None)  # Should fail
