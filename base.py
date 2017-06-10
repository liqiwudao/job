#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

import logging

from logging.handlers import RotatingFileHandler
from libs.session import RedisSessionInterface
from libs.rdstore import cache

from flask import Flask, Blueprint
from flask.views import MethodView
from mongoengine import connect

from utils.importer import find_module_classes
from views import BaseView


class NationalDay(Flask):
    mongo = None

    def init_app(self, config_obj):
        self.load_config(config_obj)
        self.load_blueprint()
        self.load_model()
        # self.load_session()
        # self.load_mako()
        self.init_logger()

    def load_session(self):
        self.session_interface = RedisSessionInterface(cache)

    def init_logger(self):
        log_level = logging.DEBUG if self.debug else self.config.get('LOG_LEVEL', 'DEBUG')
        self.logger.setLevel(log_level)
        if self.debug:
            return
        # add file handler
        if self.config.get('LOG_FILE_HANDLER'):
            from logging.handlers import RotatingFileHandler
            file_handler_config = self.config['LOG_FILE_HANDLER']
            file_handler = RotatingFileHandler(file_handler_config['filename'])
            file_handler.setLevel(file_handler_config.get('level') or log_level)
            if file_handler_config.get('format'):
                file_handler.setFormatter(logging.Formatter(file_handler_config['format']))
            self.logger.addHandler(file_handler)

    def load_config(self, config_obj, envvar='NATIONALDAY_APP_CFG'):
        self.config.from_object(config_obj)
        self.config.from_envvar(envvar, True)

    def load_model(self):
        db_name = self.config['DATABASE_NAME']
        db_host = self.config['DATABASE_HOST']
        db_port = self.config['DATABASE_PORT']
        # self.mongo = db.init_app(app=self)
        self.mongo = connect(db=db_name, host=db_host, port=db_port)

    def load_blueprint(self):
        blueprint_list = self.config['BLUEPRINT']
        for blue in blueprint_list:
            blueprint = blueprint_list[blue]
            simple_page = Blueprint(blueprint.get('name'), __name__, url_prefix=blueprint.get("url_prefix"),
                                    template_folder=blueprint.get("template"))
            self.register_blueprint(simple_page)
            for i in find_module_classes(blue, MethodView):
                obj = i
                if hasattr(obj, 'view_name'):
                    view = obj.as_view(obj.view_name)
                    self.add_url_rule(obj.url_rule, view_func=view)


def create_app(name, config, app_cls=NationalDay, **kwargs):
    app = app_cls(name, **kwargs)
    app.init_app(config)
    return app
