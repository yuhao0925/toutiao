from qiniu import Auth,put_file,etag
import qiniu.config

# 需要填写我的Access Key 和 Secret Key
access_key ='epthZxSL4mrWw63aBNIm0tg4JJP9ByWDnqIX0OHO'
secret_key = 'kOgdAeCItI66otZ3y7CLFYTUBwUXH3wvH0eMsyjM'

#  构建鉴权对象
q= Auth(access_key,secret_key)

# 要上传的空间
bucket_name = 'toutiao_flask'

# 上传后保存的文件名
file_name = None

# 生成上传Token，可以指定过期的时间
token = q.upload_token(bucket_name,key = file_name,expires=3600)
print(token)

# 要上传的文件本地路径
loacalfile = './1111.jpg'
ret,info = put_file(token,file_name,loacalfile)
print(ret)
print(info)
# assert ret['key'] ==file_name
# assert ret['hash'] == etag(loacalfile)