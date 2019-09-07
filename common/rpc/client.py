# 客户端代码
import time
import grpc
try:
    from . import reco_pb2_grpc
except:
    import reco_pb2_grpc

try:
    from . import reco_pb2
except:
    import reco_pb2



def get_grpc_func_ret(stub):
    user_request = reco_pb2.UserRequest()
    user_request.user_id = '1'
    user_request.channel_id = 1
    user_request.article_num = 10
    user_request.time_stamp = round(time.time() * 1000)


    # 通过stub调用远程服务端函数
    rpc_response = stub.user_recommend(user_request)
    print(rpc_response)
    print(rpc_response.recommends[0].track.read)
    print(rpc_response.expousre)
    return rpc_response


def run():
    #  1、通过上下文连接rpc服务端
    with grpc.insecure_channel('127.0.0.1:8888') as channel:
        #  2、实例化stub
        stub = reco_pb2_grpc.UserRecommendStub(channel)
        # 3、通过stub进行对rpc调用获取结果
        rec_response = get_grpc_func_ret(stub)
    return rec_response

if __name__ == '__main__':
    run()