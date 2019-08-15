# coding=utf-8
import os
import time

import connexion
from celery import Celery, platforms

platforms.C_FORCE_ROOT = True  # 加上这一行

# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 5}

# celery task.py需要的基本配置, 位于redis第九数据库
CELERY_BROKER_URL_TASK = "redis://127.0.0.1:6379/1"
CELERY_RESULT_BACKEND_TASK = "redis://127.0.0.1:6379/2"

CELERYD_MAX_TASKS_PER_CHILD = 2  # 设置最大处理次数

CELERY_IGNORE_RESULT = True

app = connexion.FlaskApp(__name__, specification_dir='.')
os.environ.setdefault('CELERY_TASK', '1')

if os.environ.get('CELERY_TASK'):
    # task_del_post.py
    # cd /root/backend/services/app
    # export TASK_DEL_POST=1
    # celery -A app.task_timed_del_post.celery worker -l info
    pass
else:
    app.add_api(os.environ.get('OPENAPI_CONFIG_PATH', 'openapi.yaml'), validate_responses=True)

application = app.app
# Celery configuration db 9
application.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL_TASK
application.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND_TASK

RESULT = {
    'code': 0,
    'message': 'Success',
    'data': {}
}


def make_celery(app):
    celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


# app.conf.task_default_queue = 'default'
task_routes = {
    'task.unzip': {
        'queue': 'unzip_tasks',
        'routing_key': 'unzip.import',
    },
}

celery = make_celery(app.app)
"""
cd /home/www/Github/nuo
chmod +x celery_start.sh
./celery_start.sh
celery -A  main.celery worker --concurrency=4 -l info -E -n worker1@%h -Q unzip_tasks
celery -A app.celery_app.unzip_task.celery inspect ping
"""

from celery.exceptions import SoftTimeLimitExceeded, TimeLimitExceeded  # hard timeout 一定报错


# @app.task(autoretry_for=(FailWhaleError),retry_kwargs={'max_retries': 5})

def cleanup_in_a_hurry():
    print("hard timeout")
    return "timeout"


# default_retry_delay: When a task is to be retried, it can wait for a given amount of time before doing so
# 延迟30秒重试,默认3分钟， 重试不会入队列
# 软超时为准
@celery.task(name='unzip', queue='unzip_tasks', bind=True, default_retry_delay=1, max_retries=3, time_limit=10,
             soft_time_limit=4)
def unzip(self, a, b):
    # try:
    #     # time.sleep(5)
    #     return a * b
    # except SoftTimeLimitExceeded as exc:
    #     # 重试3次还不好使，抛出异常
    #     raise self.retry(exc=exc)
    time.sleep(15)
    return a + b


from celery import Task


class MY_CELERY(Task):
    def __init__(self, name):
        self.name = name

    def run(self, x, y):
        print(self.name)
        return x + y

if __name__ == '__main__':
    """
    export CELERY_TASK=1
    celery -A  app.celery_app.publish_jingdong.celery worker --concurrency=4 -l info -E -n worker2@%h -Q publish_jingdong
    """
    my = MY_CELERY('YANGXINYUE')
    my.delay(1, 2)

    # task_id = unzip.apply_async(args=[1, 2],
    #                             queue='unzip_tasks',
    #                             routing_key='unzip.import')

    # result = task_id.wait()
    # result = unzip.delay(1, 2).get()

    # print(result)
    # print(task_id)

