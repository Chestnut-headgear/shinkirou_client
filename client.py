import requests

url = "https://shinkirou-server.onrender.com/echo"

payload = {'text':'konichiwa'}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print("response:",data['response'])
else:
    print("fuck")
