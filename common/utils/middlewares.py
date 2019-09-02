from flask import request,g
from utils.jwt_util import verify_jwt


def jwt_authentication():
    # before_request 请求钩子
    # 从请求头的Authorization中取出token, 反序列化获取user_id、refresh(是否为长效token)
    # 把user_id,refresh 放入g对象中

    g.user_id ,g.is_refresh_token = None,False  # 设置初始值
    authorization =request.headers.get('Authorization') #获取Authentication值
    # if authorization is not None:
    #     token = authorization.startswith('Bearer ')
    print(authorization)
    if authorization and authorization.startswith('Bearer '):  #startswith 返回的byes
        # token = authorization.strip('Bearer ')     #strip 返回的字符串
        token = authorization.strip()[7:]
        payload = verify_jwt(token)  # 反序列化获取layload字段
        if payload:
            g.user_id = payload.get('user_id')
            g.is_refresh_token = payload.get('refresh')