from flask_restful import Resource
from flask_limiter.util import get_remote_address
from flask import request, current_app, g
from flask_restful.reqparse import RequestParser
import random
from datetime import datetime, timedelta
from redis.exceptions import ConnectionError

from celery_tasks.sms.tasks import send_verification_code
from . import constants
from utils import parser
from models import db
from models.user import User, UserProfile
from utils.jwt_util import generate_jwt
# from cache import user as cache_user
from utils.limiter import limiter as lmt
from utils.decorators import set_db_to_read, set_db_to_write,login_required


class SMSVerificationCodeResource(Resource):
    """
    短信验证码
    """
    error_message = 'Too many requests.'

    decorators = [
        lmt.limit(constants.LIMIT_SMS_VERIFICATION_CODE_BY_MOBILE,
                  key_func=lambda: request.view_args['mobile'],
                  error_message=error_message),
        lmt.limit(constants.LIMIT_SMS_VERIFICATION_CODE_BY_IP,
                  key_func=get_remote_address,
                  error_message=error_message)
    ]

    def get(self, mobile):
        code = '{:0>6d}'.format(random.randint(0, 999999))
        current_app.redis_master.setex('app:code:{}'.format(mobile), constants.SMS_VERIFICATION_CODE_EXPIRES, code)
        send_verification_code.delay(mobile, code)
        return {'mobile': mobile}


class AuthorizationResource(Resource):
    """
    认证
    """
    method_decorators = {
        # 'post': [set_db_to_write],
        # 'put': [set_db_to_read,login_required]
    }

    def _generate_tokens(self, user_id, with_refresh_token=True):
        """
        生成token 和refresh_token
        :param user_id: 用户id
        :return: token, refresh_token
        """
        # 颁发JWT

        # 过期时间 = 当前时间+2小时
        exp = datetime.utcnow()+timedelta(hours=2)  #生成过期时间，2小时有效
        key = current_app.config['JWT_SECRET']   #密钥
        # playload = {'user_id':user_id,'refresh':False} 可以这么写，也可以下面那么写
        token = generate_jwt({'user_id': user_id, 'refresh': False}, exp, secret=key)  #token内容   refresh=Flase 表示是短效token

        refresh_token = None
        if with_refresh_token:   #长效token
            exp = datetime.utcnow() + timedelta(days=14)  # 生成过期时间，14天有效
            # playload = {'user_id':user_id,'refresh':True}
            refresh_token = generate_jwt({'user_id': user_id, 'refresh': True}, exp, secret=key)  # token内容 refresh = True 表示长效token

        return token,refresh_token


    def post(self):
        """
        登录创建token
        """
        json_parser = RequestParser()  #创建一个RequestParser对象
        # 检验 手机号和短信验证码     required=True  必须要有必须需要检查
        json_parser.add_argument('mobile', type=parser.mobile, required=True, location='json')
        json_parser.add_argument('code', type=parser.regex(r'^\d{6}$'), required=True, location='json') #短信验证码
        args = json_parser.parse_args()  #启动检查处理获取参数对象，拿到手机号，验证码
        mobile = args.mobile
        code = args.code

        # 从redis中获取验证码
        key = 'app:code:{}'.format(mobile)
        try:
            real_code = current_app.redis_master.get(key)   #master 主
        except ConnectionError as e:
            current_app.logger.error(e)
            real_code = current_app.redis_slave.get(key)    # slave 从

        try:
            current_app.redis_master.delete(key)
        except ConnectionError as e:
            current_app.logger.error(e)

        if not real_code or real_code.decode() != code:
            return {'message': 'Invalid code.'}, 400

        # 查询或保存用户
        user = User.query.filter_by(mobile=mobile).first()

        if user is None:
            # 用户不存在，注册用户
            user_id = current_app.id_worker.get_id()
            user = User(id=user_id, mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)
            profile = UserProfile(id=user.id)
            db.session.add(profile)
            db.session.commit()
        else:
            if user.status == User.STATUS.DISABLE:
                return {'message': 'Invalid user.'}, 403

        token, refresh_token = self._generate_tokens(user.id)

        return {'token': token, 'refresh_token': refresh_token}, 201



    def put(self):
        # 更新token
        # 此时客户端会带着refresh_token来请求，目的是获取token
        # 此时要把长效refresh_token放到请求头中
        if g.user_id is None:
            token ,_ = self._generate_tokens(g.user_id)  # _也可以加上长效token 看业务需求 refresh_token
            return {'token':token},201
        else:
            return {'message':'Wrong refresh token.'},403











