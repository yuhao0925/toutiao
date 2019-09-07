# 模拟 服务端
try:
    import reco_pb2_grpc
except:
    from .import reco_pb2_grpc
try:
    import reco_pb2
except:
    from .import reco_pb2
import time


class UserRecommendServicer(reco_pb2_grpc.UserRecommendServicer):

    def user_recommend(self, request, context):
        # 1.解析请求对象中的参数 request
        user_id = request.user_id
        channel_id = request.channel_id
        article_num = request.article_num
        time_stamp =  request.time_stamp
        print('接收到了rpc请求的参数')

    # 2 .构造响应对象,并且返回
        response = reco_pb2.ArticleResponse()  #实例化
        response.expousre = '曝光埋点数据'
        response.time_stamp = round(time.time()*1000)    #round() python内置函数,四舍五入取整

        recommends_list = []
        for i in range(article_num):
            article = reco_pb2.Article()   #实例化
            # article.track  不是间接关系,而是直接关系,所以track里面有的直接使用
            article.article_id = i + 1
            article.track.click = 'click'
            article.track.collect = 'collect'
            article.track.share = 'share'
            article.track.read = 'read'
            recommends_list.append(article)
        print(recommends_list)
        response.recommends.extend(recommends_list)  #因为是列表,所以用extend添加一个构造列表对象

        return response


# rpc 服务启动(执行)函数
"""
     # 1. 创建一个rpc服务器
    # 1.1 指定使用线程池处理器 concurrent.futures.ThreadPoolExecutor
    # 2. 向服务器中添加被调用的服务方法
    # 3. rpc服务绑定ip地址和端口
    # 4. 启动rpc服务，不会阻塞程序
    # 5. 不断循环防止程序退出
"""
from concurrent.futures import ThreadPoolExecutor
import grpc
import time

def server():
    server = grpc.server(ThreadPoolExecutor(max_workers=3))

    reco_pb2_grpc.add_UserRecommendServicer_to_server(UserRecommendServicer(),server)

    server.add_insecure_port('0.0.0.0:8888')

    server.start()
    while True:time.sleep(100)

if __name__ == '__main__':
    server()
