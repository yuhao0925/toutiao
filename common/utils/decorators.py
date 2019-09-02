from flask import g, current_app
from functools import wraps
from sqlalchemy.orm import load_only
from sqlalchemy.exc import SQLAlchemyError


from models import db


def set_db_to_read(func):
    """
    设置使用读数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_read()
        return func(*args, **kwargs)
    return wrapper


def set_db_to_write(func):
    """
    设置使用写数据库
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        db.session().set_to_write()
        return func(*args, **kwargs)
    return wrapper


def login_required(func):
    # 用于 装饰需要登录后才能访问的接口
    # 验证用户的user_id, 如果g对象中user_id是None, 返回401 通知客户端重新登录
    # 验证g对象中is_refresh_token是否为True, 如果为True, 返回403 通知客户端请求刷新token的接口
    @wraps(func)   # functools.wraps
    def wrapper(*args,**kwargs):
        if not g.user_id:
            return {'message':'User must be authorized.'},401
        elif g.is_refresh_token:
            return {'message':'Do not use refresh token.'},403
        else:
            return func(*args,**kwargs)
    return wrapper