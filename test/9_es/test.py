import requests

url = 'http://192.168.2.133:5000/v1_0/search?q=python&page=5&per_page=3'

resp = requests.get(url)
print(resp.json())


