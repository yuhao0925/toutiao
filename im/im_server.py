# 模拟自动聊天机器人返回数据
import time

# 模拟调用nlp聊天bot函数
def return_msg(data):
    return 'I have received your msg: {}'.format(data),\
           round(time.time()*1000)

"""
客户端向独立进程的sio服务端发送消息，服务端返回消息。
connect 连接事件
disconnect 断开连接事件
msssage   双方关注事件
"""

import eventlet
eventlet.monkey_patch()
import socketio

sio = socketio.Server(async_code = 'enventlet')


@sio.on('connect')
def connect(sid,environ):
    msg_data = {
        'msg':'hello',
        'timestamp':round(time.time()*1000)}
    sio.emit('message',msg_data,room=sid)

@sio.on('message')
def message(sid,data):
    msg,time_stamp = return_msg(data)
    msg_data = {
        'msg': 'msg',
        'timestamp': time_stamp}
    sio.emit('message',msg_data,room = sid)


import sys
if len(sys.argv)< 2 :
    port = 8090
else:
    port = int(sys.argv[1])
app = socketio.Middleware(sio)
socket = eventlet.listen(('',port))


import eventlet.wsgi
eventlet.wsgi.server(socket,app)