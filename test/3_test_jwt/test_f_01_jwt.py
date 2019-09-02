import requests,json


'''测试登录接口  POST /v1_0/authorizations'''
url = 'http://192.168.2.131:5000/v1_0/authorizations'
input('先去redis中给短信验证码。redis-cli -p 6380/6381 set app:code:13161933309 123456')
data = {'mobile': '13161933309', 'code': '123456'}
resp = requests.post(url,data=json.dumps(data),headers={'Content-Type':'application/json'})
print(resp.json())
refresh_token = resp.json()['data']['refresh_token']

'''测试 刷新token接口 PUT  /v1_0/authorizations'''
# 1.  登录 获取token 和refresh_token
# 2.  put 请求头Authorizations字段中带上Bearer refresh_token

data['Authorization'] = 'Bearer {}'.format(refresh_token)
resp = requests.put(url, headers=data)
print(resp.json())


