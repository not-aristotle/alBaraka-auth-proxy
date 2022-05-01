from flask import Flask, jsonify, current_app
from marshmallow import ValidationError

from rproxy.ext import db


def validation_error(error: 'ValidationError'):
    return jsonify({'success': False, 'messages': error.messages}), 400


def unhandled_exception(_: 'Exception'):
    current_app.logger.exception('unhandled exception')
    db.session.rollback()
    return jsonify({'success': False}), 500


def init_app(app: 'Flask'):
    app.register_error_handler(ValidationError, validation_error)
    app.register_error_handler(Exception, unhandled_exception)
    app.register_error_handler(500, unhandled_exception)
