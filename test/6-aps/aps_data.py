from datetime import datetime,timedelta
from apscheduler.executors.pool import ThreadPoolExecutor   #执行器
from apscheduler.executors.pool import ProcessPoolExecutor

from apscheduler.schedulers.background import BackgroundScheduler  #非阻塞调度器
from apscheduler.schedulers.blocking import BlockingScheduler       #阻塞

# 1、定义执行器字典（可以选择进程或者线程）
executor = {'default':ThreadPoolExecutor(max_workers=5)}#执行任务的最大线程数
            #'default':ProcessPoolExecutor(max_workers=5)
# 2、实例化调度器
scheduler = BlockingScheduler(executor = executor)
# scheduler = BackgroundScheduler(executors = executors)

# 3、添加任务
# 3.1 定义要定时执行的任务
def func(name, age):
    print('{}此时此刻{}岁了！过生日了！'.format(name, age))
# 3.2 调度器添加任务
# 3.2.1 date 触发器，只执行一次。(当前一次和下一次，最多执行2次)
# scheduler.add_job(func,'date',run_date =datetime.now()+timedelta(seconds = 5) ,args=['小明','18'])
# 3.2.2  interval触发器，周期执行，参数为时间间隔
# scheduler.add_job(func,'interval',seconds = 2,args=['小明','18'])
# 3.2.3  cron触发器，周期执行，参数为（x年）x月x日星期x，x点x分x秒执行
scheduler.add_job(func,'cron',year=2019, month=9, day=3,
                  hour=11, minute=19, second=1,args=['小明','18'])

# 4、开启定时任务
scheduler.start()