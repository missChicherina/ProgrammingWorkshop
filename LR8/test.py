import requests

# URL сервиса
base_url = 'http://127.0.0.1:5000'

# Регистрация пользователя
def register_user(username, password):
    url = f'{base_url}/user/'
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    print(response.json())

# Получение данных о пользователе
def get_user(username):
    url = f'{base_url}/user/{username}'
    response = requests.get(url)
    print(response.json())

if __name__ == '__main__':
    # Регистрация нового пользователя
    register_user('testuser', 'testpassword')
    
    # Получение данных о пользователе
    get_user('testuser')
