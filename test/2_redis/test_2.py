from redis import StrictRedis

r = StrictRedis.from_url('redis://127.0.0.1:6381/0')
p =r.pipeline()

p.set('a',100)
p.set('b',200)
p.get('a')
p.get('b')
p.get('c')

ret = p.execute()
print(ret)