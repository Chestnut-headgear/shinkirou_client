import requests

url = "http://127.0.0.1:5032/echo"

payload = {'text':'konichiwa'}

response = requests.post(url, json=payload)

if response.status_code == 200:
    data = response.json()
    print("response:",data['response'])
else:
    print("fuck")
