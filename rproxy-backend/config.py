from os import environ
from datetime import timedelta


class Config:
    LOGLEVEL = environ.get("RPROXY_LOGLEVEL", "WARNING")
    TAKE_ACCESS_TOKEN_ENDPOINT = environ.get(
        "RPROXY_TAKE_ACCESS_TOKEN_ENDPOINT",
        "https://apitest.albarakaturk.com.tr/ocf-auth-server/auth/oauth/token",
    )
    TAKE_ACCESS_TOKEN_TIMEOUT = int(
        environ.get("RPROXY_TAKE_ACCESS_TOKEN_TIMEOUT", "30")
    )
    CLIENT_ID = environ.get("RPROXY_CLIENT_ID")
    CLIENT_SECRET = environ.get("RPROXY_CLIENT_SECRET")
    API_ENDPOINT = environ.get(
        "RPROXY_API_ENDPOINT", "https://apitest.albarakaturk.com.tr/api"
    )
    API_TIMEOUT = int(environ.get("RPROXY_API_TIMEOUT", "30"))
    PRIVATE_KEY = environ.get("RPROXY_PRIVATE_KEY")
    USER_TOKEN_TTL = timedelta(
        seconds=int(environ.get("RPROXY_USER_TOKEN_TTL", "1800"))
    )
    SQLALCHEMY_DATABASE_URI = environ.get("RPROXY_SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "echo": False}
    CELERY = dict(
        broker_url=environ.get("RPROXY_CELERY_BROKER_URL"),
        broker_connection_max_retries=None,
        task_default_queue="default",
        task_routes={
            "rproxy.tasks.token.*": {
                "queue": "token",
            }
        },
        beat_schedule={
            "token-check": {
                "task": "rproxy.tasks.token.check",
                "schedule": 10,
            }
        },
    )


class DevelopmentConfig(Config):
    ...


class ProductionConfig(Config):
    ...
