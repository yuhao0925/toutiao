import requests, json

"""登录测试 POST /v1_0/authorizations"""
url = 'http://127.0.0.1:5000/v1_0/authorizations'
REDIS_SENTINELS = [('127.0.0.1', '26380'),
                   ('127.0.0.1', '26381'),
                   ('127.0.0.1', '26382'),]
REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
from redis.sentinel import Sentinel
_sentinel = Sentinel(REDIS_SENTINELS)
redis_master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
redis_master.set('app:code:13161933309', '123456')

# 构造raw application/json形式的请求体
data = json.dumps({'mobile': '13161933309', 'code': '123456'})
# requests发送 POST raw application/json 请求
resp = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
print(resp.json())
token = resp.json()['data']['token']
print(token)



"""测试上传图片接口，需要先登录"""
url = 'http://127.0.0.1:5000/v1_0/user/photo'
headers = {'Authorization': 'Bearer {}'.format(token)}
# with open('./1.png', 'rb') as f:
#     photo = f.read()
photo_obj = open('./1111.jpg', 'rb')
files_dict = {'photo': photo_obj}
resp = requests.patch(url, files=files_dict, headers=headers)
# files = {"zidingyi_name": open("./4_1_3.py", "rb")}
# r = requests.post("http://127.0.0.1:5000/upload", files=files)
print(resp.status_code)
print(resp.json())


""" 接口文档
请求参数：
PATCH/v1_0/user/photo  修改或上传用户头像图片
HEADER
     Content-Type: multipart/form-data
        Authorization: Bearer token_str
            token_str 从登录接口或刷新token接口获取
            Bearer 为固定格式，后边接上token_str，二者之间有半角空格
BODY
    photo: 接收一个可读写的文件对象
    
返回数据：
    {
    message: str类型，服务器返回的描述信息
    data: {
        photo_url: str类型，上传图片图床的url地址
        }
    }
"""