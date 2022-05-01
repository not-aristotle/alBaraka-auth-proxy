from flask import Flask

from rproxy.api.v1 import user
from rproxy.api.v1 import proxy


def init_app(app: 'Flask'):
    app.register_blueprint(user.bp, url_prefix='/api/v1/user')
    app.register_blueprint(proxy.bp, url_prefix='/api/v1/proxy')
