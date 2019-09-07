"""
服务端给客户端发生消息的方法
sio.send('消息')  群发
sio.emit('客户端监听的时间'，'消息'，room = sid or room = str)  指定发送

@sio.on('connect')  #客户端和服务端建立连接的时候会触发
@sio.on('disconnect') # 客户端和服务端断开连接时候触发

sio.enter_room(sid,room_str)  #让用户sid进入指定房间，
sid可以同时进入多个房间，也可以同时监听多个事件
sio.leave_room(sid,room_str)  #让用户sid离开指定房间
sio.room(sid)  #返回list  包含元素是sid加入的房间
"""
import eventlet.wsgi
import socketio

import eventlet
eventlet.monkey_patch()

# 创建sio服务对象
sio = socketio.Server(async_mode = 'eventlet')
# 创建使用sio服务对象的应用对象
app = socketio.Middleware(sio)
# 创建监听对象
socket = eventlet.listen(('',8090))

def run():
    eventlet.wsgi.server(socket,app)

@sio.on('connent')   #客户端和服务端建立连接时会执行
def connect(sid,envron):
    # envron是ws建立连接时，第四次握手（http1.1）时发送的请求信息
    print("建立连接 :%s" % sid)
    print(envron)


@sio.on('disconnect') #客户端和服务端断开连接时会执行
def disconnect(sid):
    print("断开连接 :%s" %sid)


@sio.on('message')   #监听自定义message，子要是自定义就接受2个参数sid，data
def message(sid,data):
    ret = "{}:{}".format(sid,data)
    print(ret)
    sio.emit('add','收到了{}'.format(ret),room=sid)
    sio.send('收到了{}'.format(ret))


@sio.on('enter_room')    #进入房间
def enter_room(sid,data):
    sio.enter_room(sid,'bt43')
    sio.emit('add','你加入了bt43的房间',room =sid)

@sio.on('get_rooms')    # 获取事件的所有
def get_rooms(sid,data):
    rooms = sio.rooms(sid)          # [ "5671c5d5993546e5943ce6038f77f337", "bt43" ]
    sio.emit('add',rooms,room='bt43')

@sio.on('leave_room')   # 离开
def leave_room(sid,data):
    sio.leave_room(sid,room='bt43')


run()



