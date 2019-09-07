from flask import current_app
from redis import RedisError
from models import db
from models.news import Article
from sqlalchemy import func

from models.user import Relation

"""zset  所有用户的发布总数
count:user:arts
发布总数=score
用户id = value

关注总数 zset 
    count:user:following
    关注总数 = score    
    用户id = value   
"""

class BaseCountStorage():
    key = ''
    @classmethod
    def get(cls,user_id):
        # 获取持久化数据
        master = current_app.redis_master
        slave = current_app.redis_slave
        try:
            ret = master.zscore(cls.key, user_id)
        except RedisError as e:
            current_app.logger.error(e)
            ret = slave.zscore(cls.key, user_id)
        if ret is None:
            return 0
        else:
            return int(ret)

    @classmethod
    def incr(cls,user_id,n = 1):
        # 让发布或关注总数(分数) +n  默认 +1
        master = current_app.redis_master
        slave = current_app.redis_slave
        try:
            master.zincrby(cls.key,user_id,n)
        except RedisError as e:
            current_app.logger.error(e)
            slave.zincrby(cls.key,user_id,n)

    @classmethod
    def reset(cls,db_query_ret):
        # 先删除持久化数据，再把db_session_ret 写入
        master = current_app.redis_master
        master.delete(cls.key)
        redis_data = []
        for user_id,count in db_query_ret:
            redis_data.append(count)
            redis_data.append(user_id)
        master.zadd(cls.key,*redis_data)



class UserArticleCountStorage(BaseCountStorage):
    """用户发布总数工具类"""
    key = 'count:user:arts'

    @staticmethod
    def db_query():
        db_query_ret = db.session.query(Article.user_id,func.count(Article.id))\
            .filter(Article.status==Article.STATUS.APPROVED)\
            .group_by(Article.user_id).all()
        return db_query_ret



class UserFollowingCountStorage(BaseCountStorage):
    """用户关注总数工具类"""
    key = 'count:user:following'

    @staticmethod
    def db_query():
        db_query_rets = db.session.query(Relation.user_id,func.count(Relation.target_user_id))\
            .filter(Relation.relation==Relation.RELATION.FOLLOW)\
            .group_by(Relation.user_id).all()