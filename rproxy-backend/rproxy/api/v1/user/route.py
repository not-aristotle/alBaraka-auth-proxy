from time import time
from os import urandom
from hashlib import sha512
from datetime import datetime, timedelta
import html
import json

from flask import request, jsonify, current_app
import requests
from requests.auth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from rproxy.api.v1.user.blueprint import bp
from rproxy.api.v1.user.schema import AuthSchema
from rproxy.ext import db
from rproxy.models import UserSession


@bp.route('/auth', methods=('POST', ))
def auth():
    data = AuthSchema().load(request.json)
    response = requests.post(current_app.config['TAKE_ACCESS_TOKEN_ENDPOINT'],
                             data={
                                 'grant_type': 'authorization_code',
                                 'code': data['code'],
                                 'redirect_uri': data['redirect_uri'],
                             },
                             auth=HTTPBasicAuth(current_app.config['CLIENT_ID'], current_app.config['CLIENT_SECRET']),
                             timeout=current_app.config['TAKE_ACCESS_TOKEN_TIMEOUT'])
    if response.status_code not in {401, }:
        response.raise_for_status()
    response = response.json()
    now = datetime.utcnow()
    try:
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        expires_in = now + timedelta(seconds=response['expires_in'])
    except KeyError:
        error_description = json.loads(html.unescape(response.get('error_description', '{}')))
        return jsonify({'success': False, 'messages': {'_schema': [error_description.get('message', 'Service Error')]}}), 200

    created = False
    try:
        user = db.session.\
            query(UserSession.user_session_id, UserSession.user_token).\
            filter(UserSession.access_token == access_token,
                   UserSession.refresh_token == refresh_token).\
            one()
    except NoResultFound:
        try:
            with db.session.begin_nested():
                user = UserSession(sha512(str(time()).encode() + urandom(128)).hexdigest(),
                                   access_token, refresh_token, expires_in, now)
                db.session.add(user)
        except IntegrityError:
            user = db.session.\
                query(UserSession.user_session_id, UserSession.user_token).\
                filter(UserSession.access_token == access_token,
                       UserSession.refresh_token == refresh_token).\
                one()
        else:
            created = True
    if not created:
        db.session.query(UserSession).\
            filter(UserSession.user_session_id == user.user_session_id).\
            update({UserSession.activated: now})
    db.session.commit()
    return jsonify({'success': True, 'user_token': user.user_token}), 200
