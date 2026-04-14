import requests


BASE_URL = "http://127.0.0.1:8000/auth"


def test_signup():
    response = requests.post(
        f"{BASE_URL}/signup",
        params={
            "email": "test@gmail.com",
            "password": "1234"
        }
    )
    print("Signup:", response.json())


def test_login(password):
    response = requests.post(
        f"{BASE_URL}/login",
        params={
            "email": "test@gmail.com",
            "password": password
        }
    )
    print("Login:", response.json())
    return response.json()


def test_profile(token):
    response = requests.get(
        f"{BASE_URL}/profile",
        params={"token": token}
    )
    print("Profile:", response.json())


# 👇 THIS MUST BE OUTSIDE FUNCTIONS
if __name__ == "__main__":

    # 1. Signup
    test_signup()

    # 2. Correct login
    data = test_login("1234")

    if "access_token" in data:
        token = data["access_token"]

        # 3. Valid profile
        test_profile(token)

        # 4. Invalid token
        test_profile("wrongtoken")

    # 5. Wrong password
    test_login("wrongpassword")