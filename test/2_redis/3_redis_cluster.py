from rediscluster import StrictRedisCluster

# redis 集群
REDIS_CLUSTER = [
    {'host': '127.0.0.1', 'port': '7000'},
    {'host': '127.0.0.1', 'port': '7001'},
    {'host': '127.0.0.1', 'port': '7002'},
]


redis_cluster = StrictRedisCluster(startup_nodes=REDIS_CLUSTER,decode_responses=True)

# redis_cluster.set('a','a1')
# ret = redis_cluster.get('a')
# print(ret)

redis_cluster.set('a','a1')   #先构造一个数据
# 1 手动获取a的值
a1 = redis_cluster.get('a')
# 2.使用管道来添加各种命令
p = redis_cluster.pipeline()
p.set('a','a2')

# 模拟a值发生改变
redis_cluster.set('a','111')


# 3.判断在集群管道执行之前，进行判断a值是否发生改变
a2 = redis_cluster.get('a')

if a2 == a1:
    #  如果没有发生变化，集群管道就执行
    ret = p.execute()
    print('以写入数据')
else:  #  如果发生变化，集群管道就不执行
    print('a值发生改变，不执行管道操作')
    pass


# redis_cluster.set('a','a1')
# p = redis_cluster.pipeline()
# p.set('a','a1')
# p.set('b','b1')
#
# input('aaa')
# p.get('a')
# p.get('b')
# ret = p.execute()
# print(ret)