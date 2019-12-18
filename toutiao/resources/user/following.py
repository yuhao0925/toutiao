# 发送关注请求的试图函数

import time
from flask_restful import Resource
from utils.decorators import login_required
from flask_restful.reqparse import RequestParser
from flask import g, current_app


class FollowingListResource(Resource):

    method_decorators = [login_required]

    def post(self):
        parser = RequestParser()
        parser.add_argument('target',required= True,
                            location = 'json',type = int,
                            help = 'target是被关注用户的user_id,int类型')
        args = parser.parse_args()
        target = str(args.target)  #被关注
        user_id = g.user_id  #发起关注

        # 构造发送的消息.(消息队列) 发送关注通知
        data = {
            'user_id':user_id,
            'timestamp':round(time.time()*1000)}

        """
        current_app.sio_maneger.emit() 只是把消息发送给mq消息队列 
               web服务向rabbitmq推送消息，消息中只有关注人的Userid
               声明该消息是要给被关注用户的user_id作为房间
        """
        current_app.sio_maneger.emit('following notify',data,room=target)
        return {'message':'已关注','data':target}
