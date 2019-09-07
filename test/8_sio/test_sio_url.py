"""
测试A关注B，B收到实时推送消息
A登录---> 拿到a的token
B登录 --->b-->token--->jwt.docode()--> 想要拿到b的user_id
A发送关注B的请求
    A 的 token  request Headers
    B 的user_id  POST  jsonbody

启动sio服务进程
B 启动sio客户端进行测试
    B----->token
"""

import requests, json

"""测试 POST /v1_0/authorizations 登录请求"""
REDIS_SENTINELS = [('127.0.0.1', '26380'),
                   ('127.0.0.1', '26381'),
                   ('127.0.0.1', '26382'),]
REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
from redis.sentinel import Sentinel
_sentinel = Sentinel(REDIS_SENTINELS)
redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
redis_master.set('app:code:18911111111', '123456')
redis_master.set('app:code:18922222222', '123456')

"""A登录"""
# 构造raw application/json形式的请求体
data = json.dumps({'mobile': '18911111111', 'code': '123456'})
# requests发送 POST raw application/json 登录请求
url = 'http://192.168.45.128:5000/v1_0/authorizations'
resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
# print(resp.json())
a_token = resp.json()['data']['token']

"""B登录"""
# 构造raw application/json形式的请求体
data = json.dumps({'mobile': '18922222222', 'code': '123456'})
# requests发送 POST raw application/json 登录请求
url = 'http://192.168.45.128:5000/v1_0/authorizations'
resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
# print(resp.json())
b_token = resp.json()['data']['token']
print(b_token)

"""B用户的user_id"""
import jwt
JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'
b_user_id = jwt.decode(b_token, JWT_SECRET, algorithm=['HS256'])['user_id']

""""""
input('别忘了启动sio服务进程；'
      '并启动firecamp测试，b用户携带token=b_token，放在url的查询字符串中；'
      '监听following notify')

"""A 发送关注B的请求"""
#     a token requestHeaders
#     b user_id POSTjsonbody
url = 'http://192.168.45.128:5000/v1_0/user/followings'
headers = {'Authorization': 'Bearer {}'.format(a_token),
           'Content-Type': 'application/json'}
import json
data = json.dumps({'target': b_user_id})
resp = requests.post(url, data=data , headers=headers)
print(resp.json())