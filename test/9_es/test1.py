import requests

url = 'http://192.168.2.133:5000/v1_0/suggestion?q=pythno'
resp = requests.get(url)
print(resp.json())


url = 'http://192.168.2.133:5000/v1_0/suggestion?q=pyth'
resp =requests.get(url)
print(resp.json())
