# -*- coding:utf-8 -*-
"""
All global objects
"""
from werkzeug.local import LocalProxy
from flask import current_app, _request_ctx_stack


def _get_current_db():
    return current_app.mongo.get_db()


def _get_current_config():
    return current_app.config


db = LocalProxy(_get_current_db)
config = LocalProxy(_get_current_config)
