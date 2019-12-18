# SIO IM服务端接口代码
"""
1、manager 消息管理对象
2、sio对象
    定义事件触发和处理方法
3、app对象
4、端口监听对象
5、执行sio服务

"""
from werkzeug.wrappers import Request
import socketio
import jwt
import eventlet
eventlet.monkey_patch()
JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'

mq_uri = 'amqp://python:rabbitmqpwd@localhost:5672/toutiao'
manager = socketio.KombuManager(mq_uri)
"""
manager消息管理对象会从mq中阻塞的取消息，一旦取到消息就会按照消息内容和约定发送
视图函数中：current_app.sio_maneger.emit('following notify', data, room=target)
所以就不用专门的执行 sio.emit('following notify', data, room=target)
"""

# 创建sio对象           client_manager=manager 给客户分发消息的消息管理对象
sio = socketio.Server(async_mode = 'eventlet',client_manager=manager)


"""定义事件触发和处理方法"""
@sio.on('connect')
def connect(sid,environ):
    # environ是建立ws连接时的第四次握手时的请求信息，走的是http1.1协议
    # 就可以规定environ的请求头信息中包含jwtoken，可以从jwtoken中取出每一个用户user_id
    # 也可以规定environ的请求url中携带jwtoken，把token放到url的查询字符串中
    request = Request(environ)
    token = request.args.get('token')

    # playload 是一个字典  按key取值，# payload = jwt.decode(token, secret, algorithm=['HS256'])
    user_id = str(jwt.decode(token, JWT_SECRET, algorithm=['HS256'])['user_id'])
    # 一旦连接sio服务，就让被关注用户加入以他的user_id命名的房间
    sio.enter_room(sid,user_id)

@sio.on('disconnect')
def disconnect(sid):
    # 用户一旦断开连接，移除全部房间
    rooms_list = sio.rooms(sid)
    for room in rooms_list:
        sio.leave_room(sid,room)


app = socketio.Middleware(sio)
socket = eventlet.listen(('',8888))
import eventlet.wsgi
eventlet.wsgi.server(socket,app)