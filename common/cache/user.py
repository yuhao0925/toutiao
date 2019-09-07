from flask import current_app
from redis import RedisError
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import load_only
import json
from models.user import User
from . import constants
# from cache import constants


class UserProfileCache():
    key = 'user:{}:profile'

    def get(self,user_id):
        # 根据用户id查询缓存，返回用户信息
        # 先查询redis缓存记录
            # 如果有记录直接返回
            # 如果没有记录，就查询数据库
                # 如果数据库中没有记录，设置redis保存不存在的记录为 -1 防穿透
                # 如果数据库中有记录，就设置redis记录 string
        # 返回 字典 {手机号 昵称 头像 认证 简介}
        r = current_app.redis_cluster
        # 先查询redis缓存记录
        try:
            ret = r.get(self.key.format(user_id))
        except RedisError as e:
            current_app.logger.error(e)
            ret = None
        # 如果没有记录，就查询数据库
        if ret is None:
            try:
                db_ret = User.query.options(load_only(
                    User.name,         # 不设置的话会查询所有，查询速度变慢，指定需要查询的字段，会优化查询速度
                    User.profile_photo,
                    User.certificate,
                    User.introduction
                )).filter(User.id == user_id).first()
            except DatabaseError as e:
                current_app.logger.error(e)
                raise e
            # 如果数据库中有记录，就设置redis记录 string
            print(db_ret)
            if db_ret is not None:
                ret_dict = {
                    'user_name': db_ret.name,
                    'user_photo': db_ret.profile_photo,
                    'certificate': db_ret.certificate,
                    'introduction': db_ret.introduction,
                }
                # 设置过期时间
                # 过期时间设置位2-2个半小时
                try:
                    r.setex(self.key.format(user_id),constants.UserCacheTTL.get_TTL(),ret_dict)
                except RedisError as e:
                    current_app.logger.error(e)
                return ret_dict

            # 如果数据库中没有记录,设置redis保存不存在的记录为 -1 防穿透
            else:
                # 过期时间缓存设置5-10分
                try:
                    r.setex(self.key.format(user_id),constants.UserNotExistCacheTTL.get_TTL(),'-1')
                except RedisError as e:
                    current_app.logger.error(e)
                return None
        # 如果有记录直接返回
        if ret == '-1':
            return None
        else:

            """
             b"{'user_name': '13161933309', 'user_photo': 'FkKSYfsEqp5alR3MWTxjd4Dy7u2k', 'certificate': None, 'introduction': None}"
            如果要把json字符串转换成dict list的话
            1.json字符串内部使用引号问题
            2.json字符串内部不能存在None null nil
            3.replace('None', '""')
            """
            ret = str(ret, encoding='utf-8').replace("'", '"').replace('None', '""')  #replace 替换
            print(ret)
            return json.loads(ret)   #坑


    def clear(self,user_id):
        # 根据用户id删除指定的key
        key = self.key.format(user_id)
        r = current_app.redis_cluster
        r.delete(key)


    def exists(self,user_id):
        # 根据用户id判断用户是否存在
        # 先查询redis缓存记录
            # 如果有记录直接返回True
            # 如果没有记录，就查询数据库
                #如果数据库中有记录，就设置redis记录，返回True
                # 如果数据库中没有记录，就设置redis保存不存在的记录为-1，返回False，反正穿透
        ret = self.get(user_id)
        if ret is None:
            return False
        else:
            return True