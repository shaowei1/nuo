import gevent
import time
from gevent import monkey

# 打补丁，让gevent框架识别耗时操作，比如：time.sleep，网络请求延时
monkey.patch_all()


# 任务1
def work1(num):
    for i in range(num):
        print("work1....")
        # time.sleep(0.2)
        gevent.sleep(0.2)


# 任务1
def work2(num):
    for i in range(num):
        print("work2....")
        # time.sleep(0.2)
        gevent.sleep(0.2)


if __name__ == '__main__':
    # 创建协程指定对应的任务
    g1 = gevent.spawn(work1, 3)
    g2 = gevent.spawn(work2, 3)

    # 主线程等待协程执行完成以后程序再退出
    g1.join()
    g2.join()
    # 　也可私用joinall(param)
    # param: A sequence (supporting :func:`len`) of greenlets to wait for.
    #  gevent.joinall([g1, g2])
