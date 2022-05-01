from os import environ

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from Crypto.PublicKey import RSA

from rproxy.ext import db
from rproxy.api import v1
from rproxy import error, tasks


def create_app() -> "Flask":
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(environ["RPROXY_CONFIG"])
    if app.config["PRIVATE_KEY"]:
        with open(app.config["PRIVATE_KEY"], "rb") as private_key:
            app.config["PRIVATE_KEY"] = RSA.importKey(private_key.read())
    app.logger.setLevel(app.config["LOGLEVEL"])
    db.init_app(app)
    tasks.init_app(app)
    v1.init_app(app)
    error.init_app(app)
    return app
