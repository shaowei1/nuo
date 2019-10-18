from flask_marshmallow import Marshmallow
import connexion
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
import traceback
from decimal import Decimal

from flask import jsonify
from sqlalchemy.orm import joinedload
import os

from celery.exceptions import SoftTimeLimitExceeded
from celery import Celery, platforms

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = os.getenv('MYSQL_PORT', 3306)
MYSQL_USERNAME = os.getenv('MYSQL_USERNAME', 'username')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'ecpro')

CELERY_BROKER_URL_TASK = os.getenv('CELERY_BROKER_URL_TASK', 'ecpro')
CELERY_RESULT_BACKEND_TASK = os.getenv('CELERY_RESULT_BACKEND_TASK', 'ecpro')
os.environ.setdefault('CELERY_TASK', '1')

basedir = os.path.abspath(os.path.dirname(__file__))
# 为用户点击购买的时候生成训练标签锚点等数据
# app = connexion.FlaskApp(__name__, specification_dir='.')
app = connexion.FlaskApp(__name__, specification_dir=basedir)

application = app.app

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(MYSQL_USERNAME,
                                                                                               MYSQL_PASSWORD,
                                                                                               MYSQL_HOST, MYSQL_PORT,
                                                                                               MYSQL_DATABASE)
application.config['SQLALCHEMY_POOL_RECYCLE'] = 3600
application.config['SQLALCHEMY_POOL_SIZE'] = 20
application.config['SQLALCHEMY_POOL_PRE_PING'] = True
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_ECHO'] = True

# Celery configuration db 9
application.config['CELERY_BROKER_URL'] = CELERY_BROKER_URL_TASK
application.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND_TASK

mysql_store = SQLAlchemy(app.app)


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


CELERYD_MAX_TASKS_PER_CHILD = 40  # 设置最大处理次数
CELERY_IGNORE_RESULT = True
platforms.C_FORCE_ROOT = True

celery = make_celery(app.app)


@celery.task(name="publish_jingdong", queue='publish_jingdong')
def publish_jingdong_product(**kwargs):
    pass
