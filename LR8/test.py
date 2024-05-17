import requests

url = 'http://127.0.0.1:5000/user/'
data = {
    "username": "testuser",
    "password": "testpassword"
}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
