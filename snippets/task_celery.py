from __future__ import absolute_import, unicode_literals
from celery import Celery

celery = Celery(
    'myapp',
    broker='redis://127.0.0.1:6379/1',
    # ## add result backend here if needed.
    # backend='rpc'
)


class my():
    def __init__(self, name):
        self.name = name

    @celery.task()
    def add(self, x, y):
        print(self.name)
        return x + y


if __name__ == '__main__':
    m = my('yangxinyue')
    m.add.delay(x=1, y=2)

    # app.start()
