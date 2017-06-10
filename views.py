#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'


from flask import Flask, request, render_template
from flask.views import MethodView
from decorators import require_login, auth_login, backup_auth

class BaseView(MethodView):
    template_base = 'app'
    decorators = [require_login]

class BackUpView(MethodView):
    template_base = 'dashboard'
    decorators = [backup_auth]

class BackInitView(MethodView):
    template_base = 'dashboard'
    decorators = []

class AuthView(MethodView):
    decorators = []

class InitView(MethodView):
    template_base = 'app'
    decorators = []


class LoginView(MethodView):
    template_base = 'app'
    decorators = [auth_login]




class BaseApiView(MethodView):
    decorators = []



