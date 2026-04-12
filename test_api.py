import requests

BASE_URL = "http://localhost:8000"

print("=" * 50)
print("TESTING USER AUTHENTICATION API")
print("=" * 50)

# Test 1: Signup new user
print("\n📝 TEST 1: Signup new user")
response = requests.post(f"{BASE_URL}/auth/signup", params={
    "email": "alice@test.com",
    "password": "alice123"
})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Duplicate signup (should fail)
print("\n📝 TEST 2: Duplicate signup (should fail)")
response = requests.post(f"{BASE_URL}/auth/signup", params={
    "email": "alice@test.com",
    "password": "different"
})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 3: Login with correct credentials
print("\n📝 TEST 3: Login with correct credentials")
response = requests.post(f"{BASE_URL}/auth/login", params={
    "email": "alice@test.com",
    "password": "alice123"
})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 4: Login with wrong password (should fail)
print("\n📝 TEST 4: Login with wrong password (should fail)")
response = requests.post(f"{BASE_URL}/auth/login", params={
    "email": "alice@test.com",
    "password": "wrong"
})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 5: Signup with empty password (should fail)
print("\n📝 TEST 5: Signup with empty password (should fail)")
response = requests.post(f"{BASE_URL}/auth/signup", params={
    "email": "bob@test.com",
    "password": ""
})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n" + "=" * 50)
print("✅ TESTING COMPLETE")
print("=" * 50)