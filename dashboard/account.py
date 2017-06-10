#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

from flask import request, abort, render_template, session

from views import BackInitView


# from models.classes import Class
# from models.content import Content
# from models.tag import Tag


class AccountView(BackInitView):
    url_rule = '/dashboard/login/'
    view_name = 'dashboard_account'

    def get(self):
        return render_template('%s/login/login.html' % self.template_base)
        # return render_template('base.html')
