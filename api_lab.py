import requests

BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print(f"\n===={title}====")

def signup(email, password):
    return requests.post(
        f"{BASE_URL}/auth/signup", params={"email": email, "password": password}).json()

def login(email, password):
    return requests.post(
        f"{BASE_URL}/auth/login", params={"email": email, "password": password}).json()

def create_task(token, title):
    return requests.post(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": title, "completed": False}
    ).json()

def get_tasks(token):
    return requests.get(
        f"{BASE_URL}/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

def test_normal_flow():
    print_section("NORMAL FLOW")

    signup("a@test.com", "1234")
    signup("b@test.com", "1234")

    user_a = login("a@test.com", "1234")
    user_b = login("b@test.com", "1234")

    token_a = user_a["access_token"]
    token_b = user_b["access_token"]

    print("User A creating tasks...")
    create_task(token_a, "Task A1")
    create_task(token_a, "Task A2")

    print("User B creating tasks...")
    create_task(token_b, "Task B1")

    print("User A tasks:", get_tasks(token_a))
    print("User B tasks:", get_tasks(token_b))

def test_attacks(token_a, token_b):
    print_section("ATTACK TESTS")

    print("No token:")
    print(requests.get(f"{BASE_URL}/tasks/").json())

    print("Fake token:")
    print(get_tasks("fake_token"))

    print("Cross user access (manual check):")
    print("User B should NOT see A tasks")
    print(get_tasks(token_b))

if __name__ == "__main__":
    test_normal_flow()

    user_a = login("a@test.com", "1234")
    user_b = login("b@test.com", "1234")

    test_attacks(user_a["access_token"], user_b["access_token"])

    token = user_a["access_token"]
    print(create_task(token, "Background Task Test"))
