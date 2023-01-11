from time import timezone
from celery import Celery

def make_celery(app):
    celery = Celery("Application Jobs", broker="redis://localhost:6379/1", backend= "redis://localhost:6379/2")
    #disable UTC
    celery.conf.enable_utc = False
    celery.conf.update(timezone="Asia/Kolkata")
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery