# -*- coding:utf-8 -*-
import logging
from flask import current_app
from werkzeug.local import LocalProxy


def _get_app_logger():
    return current_app.logger


app_logger = LocalProxy(_get_app_logger)
