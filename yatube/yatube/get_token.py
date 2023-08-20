import requests

url = 'http://127.0.0.1:8000/api-token-auth/'
data = {
    'username': 'arno', 
    'password': 'ZakImp1899'  
}

response = requests.post(url, data=data)

if response.status_code == 200:
    token = response.json()['token']
    print('Token:', token)
else:
    print('Failed to get token:', response.status_code)