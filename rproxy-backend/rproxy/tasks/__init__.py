from flask import Flask
from celery.app.task import Task

from rproxy.ext import celery
from rproxy.tasks import token


def init_app(app: "Flask"):
    celery.conf.update(app.config["CELERY"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    setattr(celery, "Task", ContextTask)


@celery.task(name="rproxy.tasks.token.check", bind=True)
def rproxy_tasks_token_check(self: "Task"):
    token.check(self)


@celery.task(name="rproxy.tasks.token.refresh", bind=True)
def rproxy_tasks_token_refresh(self: "Task", user_session_id: "int"):
    token.refresh(self, user_session_id)
