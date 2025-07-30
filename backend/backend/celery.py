from celery import Celery, Task
import sys
import os

def celery_init_App(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.conf.update(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/1',
        timezone='Asia/Kolkata',
        enable_utc=False,
        broker_connection_retry_on_startup=True,
    )
    celery_app.set_default()
    app.extensions['celery'] = celery_app

    # Set IST time in Celery logs
    import logging
    import pytz
    from datetime import datetime

    class ISTFormatter(logging.Formatter):
        converter = lambda *args: datetime.now(pytz.timezone("Asia/Kolkata")).timetuple()
        def formatTime(self, record, datefmt=None):
            ct = self.converter(record.created)
            if datefmt:
                s = datetime.fromtimestamp(record.created, pytz.timezone("Asia/Kolkata")).strftime(datefmt)
            else:
                s = datetime.fromtimestamp(record.created, pytz.timezone("Asia/Kolkata")).isoformat()
            return s

    formatter = ISTFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    for handler in logging.root.handlers:
        handler.setFormatter(formatter)

    return celery_app
