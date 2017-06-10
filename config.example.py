#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'
import logging

DATABASE_NAME = 'filmslate'
DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 27017

SECRET_KEY = 'astjqio3bj6oiq3406#@$^#@$^#'

# MONGODB_DB = 'nationalday'
# MONGODB_HOST = 'localhost'
# MONGODB_PORT = 27017
#


REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = '0'

BLUEPRINT = {
    "home": {
        'name': 'test',
        'url_prefix': '/',
        'template': 'templates'
    },
    "nationalday_api": {
        'name': 'test2',
        'url_prefix': '/api/',
    },
    "dashboard": {
        'name': 'dashboard',
        'url_prefix': '/dashboard/',
    }
}

DEBUG = True

LOG_LEVEL = logging.INFO

LOG_FILE_HANDLER = {
    'filename': './nationalday.log'
}

QINIU = {
    'access_key': '',
    'secret_key': '',
    'bucket_name': '',
    'url': '',
}
