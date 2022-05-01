from rproxy import create_app
from rproxy.tasks import celery


flask_app = create_app()
celery_app = celery
