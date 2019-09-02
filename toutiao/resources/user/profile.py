from flask import g,current_app
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from models import db
from models.user import User
from utils.decorators import login_required
from utils.parser import image_file
from utils.storage import upload_image


class PhotoResource(Resource):
    # 使用装饰器验证
    method_decorators = [login_required]

    def patch(self):
        # 获取参数并进行检查
        rp= RequestParser()
        rp.add_argument('photo',type= image_file,required = True,location = 'files')
        args_dict = rp.parse_args()
        photo = args_dict['photo']

        # 上传图片到七牛云，获取图片key
        file_name = upload_image(photo.read())
        # 把图片数据保存到数据库
        User.query.filter(User.id==g.user_id).update({'profile_photo':file_name})
        # 上传，提交
        db.session.commit()
        # 把图片的完整url返回
        # photo_url = current_app.config['QINIU_DOMAIN']+file_name
        # return {'photo_url':photo_url}
        ret_dict = {
            'photo_url':'{}/{}'.format(current_app.config['QINIU_DOMAIN'],file_name)}
        return ret_dict