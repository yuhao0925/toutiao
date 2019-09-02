import jwt
from jwt import PyJWTError
from datetime import datetime,timedelta
import time

# 自定义秘钥
key = 'secret'

# 自定义载荷
data = {
    'playload':'test',    #exp 过期时间
    'exp':datetime.utcnow()+timedelta(seconds=10)}    #  datetime.utcnow() 当前时间  timedelta(seconds=10) 多久过期
    # 'exp':datetime.utcnow()+timedelta(seconds=1)}
# 生成token                                 algorithm 加密方式
token = jwt.encode(payload = data,key = key,algorithm='HS256')
print(token)

time.sleep(1.5)

# 验证
try:
    ret = jwt.decode(token,key,algorithms='HS256')
    print(ret)
except PyJWTError as e:
    print('jwt认证失败')