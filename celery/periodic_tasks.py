from __future__ import absolute_import, print_function, unicode_literals

from celery import Celery
from celery.schedules import crontab

app = Celery(
    # XXX The below 'myapp' is the name of this module, for generating
    # task names when executed as __main__.
    'periodic_tasks',
    broker='redis://127.0.0.1:6379/1',
    # ## add result backend here if needed.
    # backend='rpc'
)

app.conf.timezone = 'UTC'


@app.task(name='periodic_tasks', queue='say')
def say(what):
    """
     ps -ef | grep app.celery_app.authorized_detect.celery | awk '{print $2}' | xargs kill -9
    sent message: celery -A periodic_tasks beat -l info
    receive message: celery -A periodic_tasks worker -l info -Q say
    """
    print(what)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls say('hello') every 10 seconds.
    sender.add_periodic_task(10.0, say.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, say.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        say.s('Happy Mondays!'),
    )
    # See periodic tasks user guide for more examples:
    # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html


if __name__ == '__main__':
    app.start()
