import random

class BaseCacheTTL():
    # 缓存有效期，单位是秒，要防止雪崩
    TTL = 60 * 60 * 2  #基础过期时间
    MAX_DELTA = 60 * 30   #随机时间上限

    # @classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
    @classmethod
    def get_TTL(cls):
        # 返回有效期时间范围内的随机值
        return cls.TTL + random.randrange(0,cls.MAX_DELTA)


#  为了防止雪崩，在不同的数据设置缓存有效期时采用设置不用的有效期方案，
# 所以采用继承的方式
class UserCacheTTL(BaseCacheTTL):
    # 用户信息缓存数据过期时间
    pass

# 不存在的用户信息缓存过期时间5-10分钟，防穿透
class UserNotExistCacheTTL(BaseCacheTTL):
    TTL = 60 * 5    #基础过期时间
    MAX_DELTA = 60 * 5   #随机时间上限