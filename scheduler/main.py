from apscheduler.executors.pool import ThreadPoolExecutor   #执行器

from apscheduler.schedulers.blocking import BlockingScheduler       #阻塞
import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,os.path.join(BASE_DIR,'common'))
sys.path.insert(0,os.path.join(BASE_DIR))

from cache.statistic import UserArticleCountStorage,UserFollowingCountStorage
from toutiao import create_app
from settings.default import DefaultConfig


# 1、定义执行器字典（可以选择进程或者线程）
executor = {'default':ThreadPoolExecutor(3)}#执行任务的最大线程数

# 2、实例化调度器
scheduler = BlockingScheduler(executor=executor)


# 定义任务函数

flask_app = create_app(DefaultConfig)
def func():
    #查询数据库 reset持久化数据 发布总数数据
    with flask_app.app_context():
        db_query_ret = UserArticleCountStorage.db_query()
        UserArticleCountStorage.reset(db_query_ret)
    #   对用户关注总数进行数据同步 ....


# 3、添加定时任务
#  cron触发器
# scheduler.add_job(func,'cron',hour= 3)
scheduler.add_job(func,'cron')   # 测试专用

# 4、开启定时任务
if __name__ == '__main__':

    scheduler.start()