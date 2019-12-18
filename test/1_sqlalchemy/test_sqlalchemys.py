from datetime import datetime
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, not_, func
from sqlalchemy.orm import load_only,contains_eager

app = Flask(__name__)
# step 1. 配置sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql@127.0.0.1:3306/toutiao' # 数据库连接地址
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 是否追踪数据库修改, 开启后影响性能
app.config['SQLALCHEMY_ECHO'] = True  # 开启后, 可以在控制台打印底层执行的sql语句

# step 2. 创建数据库连接对象
db = SQLAlchemy(app)

class User(db.Model):
    '''
    用户基本信息
    '''
    __tablename__ = 'user_basic'

    class STATUS:
        ENABLE = 1
        DISABLE = 0

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户id')
    account = db.Column(db.String,doc='账号')
    email = db.Column(db.String,doc='邮箱')
    status = db.Column(db.Integer,default=1,doc='状态,是否可用')
    mobile = db.Column(db.String,doc='手机号')
    password = db.Column(db.String,doc='密码')
    name = db.Column('user_name',db.String,doc='昵称')
    profile_photo = db.Column(db.String,doc='头像')
    last_login =db.Column(db.DateTime,doc='最后登录时间')
    is_media =db.Column(db.Boolean,default=False,doc='是否是自媒体')
    is_verified = db.Column(db.Boolean,default=False,doc='是否实名认证')
    introduction = db.Column(db.String,doc='简介')
    certificate = db.Column(db.String,doc='认证')
    article_count = db.Column(db.Integer,default=0,doc='发文章数(发帖数)')
    following_count =db.Column(db.Integer,default=0,doc='关注的人数')
    fans_count =db.Column(db.Integer,default=0,doc='被关注的人数(粉丝数)')
    like_count =db.Column(db.Integer,default=0,doc='累计点赞人数')
    read_count =db.Column(db.Integer,default=0,doc='累计阅读人数')

    # 方式1
    # profile = db.relationship('UserProfile',uselist = False)
    # 方式2
    profile = db.relationship('UserProfile',
                              primaryjoin = 'User.id==foreign(UserProfile.id)',uselist = False)

class UserProfile(db.Model):
    '''
    用户资料表
    '''
    __tablename__ = 'user_profile'

    class GENDER:
        ENABLE = 1
        DISABLE = 0

    # 方式1
    # id = db.Column('user_id',db.Integer, db.ForeignKey('user_basic.user_id'),primary_key=True)
    id = db.Column('user_id',db.Integer,primary_key=True)
    gender = db.Column(db.String,default=0,doc='性别')
    birthday = db.Column(db.DateTime,doc='生日' )
    real_name = db.Column(db.String, doc='真实姓名')
    id_number = db.Column(db.String, doc='身份证号')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    ctime=db.Column('create_time',db.DateTime,default=datetime.now,doc='创建时间')
    utime = db.Column('update_time',db.DateTime,default=datetime.now,onupdate=datetime.now, doc='更新时间')
    register_media_time = db.Column(db.DateTime, doc='注册自媒体时间')
    area = db.Column(db.String, doc='地区')
    company = db.Column(db.String, doc='公司')
    career =db.Column(db.String, doc='职业')

class Relation(db.Model):
    '''
    用户关系表
    '''
    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    target_user_id= db.Column(db.Integer, doc='目标用户ID')
    relation = db.Column(db.Integer, doc='关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')


#--------------ORM SQL语句操作-------------
@app.route('/get_all')
def get_all():
    # 查询所有用户
    # users = User.query.all()
    users = db.session.query(User).all()
    ret_dict = {}
    for user in users:
        ret_dict[user.mobile] = user.name
    return jsonify(ret_dict)

# 查询第一个,返回对象
@app.route('/first')
def first():
    # user = User.query.first()
    user = db.session.query(User).first()
    return jsonify({user.mobile:user.name})

@app.route('/get')
def get():
    # 根据主键ID获取对象，若主键不存在返回None
    user = db.session.query(User).get(2)
    # user = User.query.get(3)
    return jsonify({user.mobile:user.name})


@app.route('/filter_by')
def filter_by():
    User.query.filter_by(mobile = '18516952650').first()
    ret = User.query.filter_by(mobile = '18516952650',id = 1).first()
    return ret.name


@app.route('/filter')
def filter():
    ret = User.query.filter(User.mobile=='18516952650').first()
    return ret.name

# or_逻辑或
@app.route('/or')
def o_r():
    rets = User.query.filter(or_(User.mobile=='13911111111',User.name.endswith('号'))).all() #.all()  #获取多个  or_ 或的意思
    ret_dict = {ret.mobile:ret.name for ret in rets}
    # return rets.name   #获取一个
    return jsonify(ret_dict)


# and_ 逻辑与
@app.route('/and')
def an_d():
    rets = User.query.filter(and_(User.name != '13911111111',User.mobile.startswith('185'))).all()
    ret_dict = {ret.mobile:ret.name for ret in rets}
    # return rets.name
    return jsonify(ret_dict)


@app.route('/not')
def n_ot():
    rets = User.query.filter(not_(User.mobile == '13911111111')).all()
    ret_dict = {ret.mobile:ret.name for ret in rets}
    return jsonify(ret_dict)


@app.route('/offset')
def offset():
    # 跳过第二个,从第三个开始  offset
    rets = User.query.offset(2).all()
    ret_dict = {ret.id:ret.name for ret in rets}
    return jsonify(ret_dict)


@app.route('/limit')
def limit():
    # limit(n) 自选取n个
    rets = User.query.limit(5).all()
    # ret_dict = {ret.id:ret.name for ret in rets}
    # return jsonify(ret_dict)
    return rets.name



@app.route('/order_by')
def order_by():
    # desc 倒序
    rets1 = User.query.order_by(User.id.desc()).all() #根据id倒序
    rets2 = User.query.order_by(User.id).all()  #正序
    ret_dict={'a':str(rets1),'b':str(rets2)}
    return jsonify(ret_dict)


@app.route('/fuhe')
def fuhe():
    # 倒序查询 跳过2个  一共获取5个
    # 方法1
    rets = User.query.filter(User.name.startswith('13')).order_by(User.id.desc())\
    .offset(2).limit(5).all()
    rest_dict = {ret.id:ret.name for ret in rets}
    return jsonify(rest_dict)
    # 方法2
    # query = User.query.filter(User.name.startswith('13'))
    # query = query.order_by(User.id.desc())
    # query = query.offset(2).limit(4)
    # rets = query.all()
    # return str(User.name.rets)


@app.route('/youhua')
def youhua():
    # print('==')
    # load_only表示只读取字段，不整条数据查询
    ret = User.query.options(load_only(User.name,User.mobile)).filter_by(id=1).first()
    User.query.filter_by(id =1).first()
    # print('==')
    return '{}:{}'.format(ret.name,ret.mobile)

@app.route('/juhe')
def juhe():
    # 聚合查询使用func模块
    # 查询关注别人的用户id，和他关注的总人数
    # 1.从uesr_relation表中，获取relation==1的所有数据
    # 2. 根据发起关注的人id进行分组
    # 对每组的数据表数据进行统计，得出发起关注人数的id，多少条数据
    # 分组 group_by
    rets = db.session.query(Relation.user_id,func.count(Relation.target_user_id))\
        .filter(Relation.relation==Relation.RELATION.FOLLOW)\
        .group_by(Relation.user_id).all()
    # rets = [(1, 3), (2, 1), (33, 1), (61, 1)]
    return str(rets)

@app.route('/gender')
def gender():
    # user = User.query.filter(User.mobile=='15174471887').first()
    # return str(user.profile.gender)

    # 指定字段进行关联查询
    rets = User.query.join(User.profile)\
        .options(load_only(User.mobile),
                 contains_eager(User.profile).load_only(UserProfile.gender))\
        .filter(User.mobile == '15174471887').first()
    print(rets)
    return str(rets.profile.gender)

# 更新
@app.route('/update')
def update():
    # 方式1
    user = User.query.get(2)
    user.name='绝地求生2'
    db.session.add(user)
    db.session.commit()
    # 方式2
    input('aaa')
    User.query.filter_by(id =1).update({'name':'黑马头条号2'})
    db.session.commit()

    return 'update'

@app.route('/delete')
def delete_data():
    User.query.filter(User.mobile=='15174471887').delete()
    db.session.commit()

    # user = User.query.get(1102490522829717507) #关联了外键，想删除的化要将关联的外键也要一起删除
    # db.session.delete(user)
    # db.session.commit()
    # return 'delete'


@app.route('/shiwu')
def shiwu():
    try:
        user = User(mobile='18911111111',name='itheima')
        db.session.add(user)
        db.session.flush() #flush意思是将db.session记录的sql传到数据库中执行
        profile = UserProfile(id = user.id)
        db.session.add(profile)
        db.session.commit()
    except:
        db.session.rollback()  # 报错就回滚
    return 'shiwu'




@app.route('/add')
def data_add():
    # 增加数据
    user= User(mobile='15174471887', name='紫棋姐姐11')
    db.session.add(user)
    db.session.commit()
    profile = UserProfile(id = user.id)
    db.session.add(profile)
    db.session.commit()

    return 'data_add'

@app.route('/')
def index():
    a = app.url_map.iter_rules()
    rules_iterator = app.url_map.iter_rules()
    return jsonify(
        {rule.endpoint: rule.rule for rule in rules_iterator if rule.endpoint not in ('route_map', 'static')})

@app.route('/offset_limit')
def offset_limit():
    rets = User.query.filter(not_(User.name.endswith('号'))).offset(2).limit(1).all()
    return rets[0].name

@app.route('/update1')
def update1():
    user = User.query.get(2)
    user.name='yuhao'
    db.session.add(user)
    db.session.commit()
    return 'aaaaa'

@app.route('/delete1')
def delete1():
    user = User.query.filter(User.name=='18922222222').delete()
    db.session.commit()
    return 'delete'

if __name__ == '__main__':
    # db.drop_all()  # 删除所有继承自db.Model的表
    # db.create_all()  # 创建所有继承自db.Model的表 # 在这里建立了表格
    app.run(debug=True)