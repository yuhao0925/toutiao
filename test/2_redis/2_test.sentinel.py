from redis.sentinel import Sentinel
REDIS_SENTINELS = [
    ('127.0.0.1', '26380'),
    ('127.0.0.1', '26381'),
    ('127.0.0.1', '26382'),
]
REDIS_SENTINEL_SERVICE_NAME = 'mymaster' # 哨兵配置中主从集群的名字
#   decode_responses 默认等于Flase
_sentinel = Sentinel(REDIS_SENTINELS, decode_responses=True)
# 主从redis连接对象 返回的就不是byes类型
master = _sentinel.master_for(REDIS_SENTINEL_SERVICE_NAME)
slave = _sentinel.slave_for(REDIS_SENTINEL_SERVICE_NAME)
# 正常操作redis数据，命令不变
# ret = master.set('b', '222')

# 非事务命令管道
# p = master.pipeline(transaction=False)

# 也可以使用事务管道操作，本质是python的redis模块代码实现的
p = master.pipeline()
p.multi()
p.set('a', '111')
p.get('a')
ret = p.execute()
print(ret)

