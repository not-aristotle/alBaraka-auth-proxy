from flask_sqlalchemy import SQLAlchemy
from celery import Celery


db = SQLAlchemy()
celery = Celery(__name__.rsplit('.', 1)[0])
