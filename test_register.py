import requests

API_URL = "http://127.0.0.1:8002"
username = "najla"
password = "123"

res = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
print(res.status_code, res.json())
