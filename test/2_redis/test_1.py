from redis import StrictRedis,WatchError

# r = StrictRedis.from_url('redis://127.0.0.1:6381/0')
r = StrictRedis(host='127.0.0.1',port=6381,db=0,decode_responses=True)
# 1 创建命令管道
# p = r.pipeline()
# # 向管道添加数据
# p.set('a',10)
# p.set('b',20)
# p.get('a')
# p.get('b')
# ret = p.execute()
# print(ret)

'''watch监视'''

r.set('key1','hahaha') #设置测试
p = r.pipeline()
try:
    p.watch('key1')  #监听k
    print(p.get('key1'))
    r.set('key1','heihei')
    print(p.get('key1'))
    p.multi()
    p.set('key1')
    ret = p.execute()
    print(ret)
except WatchError as e:
    print(e)