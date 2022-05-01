from datetime import datetime, timedelta

from celery.app.task import Task
from celery.utils.log import get_task_logger
from celery import signature
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm.exc import NoResultFound
from flask import current_app

from rproxy.ext import db
from rproxy.models import UserSession


def check(self: 'Task'):
    expires = datetime.utcnow() + timedelta(seconds=30)
    expired_users = db.session.\
        query(UserSession.user_session_id).\
        filter(UserSession.expires <= expires).\
        all()
    for user in expired_users:
        signature('rproxy.tasks.token.refresh', app=self.app).delay(user.user_session_id)


def refresh(self: 'Task', user_session_id: 'int'):
    logger = get_task_logger(__name__)
    try:
        user = db.session.\
            query(UserSession.refresh_token).\
            filter(UserSession.user_session_id == user_session_id).\
            one()
    except NoResultFound:
        return
    try:
        response = requests.post(current_app.config['TAKE_ACCESS_TOKEN_ENDPOINT'],
                                 data={
                                     'grant_type': 'refresh_token',
                                     'refresh_token': user.refresh_token
                                 },
                                 auth=HTTPBasicAuth(current_app.config['CLIENT_ID'], current_app.config['CLIENT_SECRET']),
                                 timeout=current_app.config['TAKE_ACCESS_TOKEN_TIMEOUT'])
        logger.info(response.text)
        response.raise_for_status()
        response = response.json()
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        expires_in = response['expires_in']
    except (IOError, ValueError, KeyError):
        logger.info('{} lost token'.format(user_session_id), exc_info=True)
        db.session.\
            query(UserSession).\
            filter(UserSession.user_session_id == user_session_id).\
            delete()
    else:
        logger.info('{} got new token'.format(user_session_id))
        db.session.\
            query(UserSession).\
            filter(UserSession.user_session_id == user_session_id).\
            update({UserSession.access_token: access_token,
                    UserSession.refresh_token: refresh_token,
                    UserSession.expires: datetime.utcnow() + timedelta(seconds=expires_in)})
    db.session.commit()
