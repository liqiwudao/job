#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

from flask import request, make_response, render_template, abort

from views import InitView, BaseView
from models.account import Account
import json


class UserView(BaseView):
    url_rule = '/login/signin/'
    view_name = 'login_signin'

    def get(self, **kwargs):
        return render_template('%s/account/signin.html' % (self.template_base), msg=kwargs.get("msg"))


