#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zjw'

import random
from flask import request, session, redirect, url_for
from views import AuthView
# import json
import hmac
from api.utils import success, bad_request
from libs.rdstore import cache
# from models.auth import AuthApi
from models.admin import AdminAccount
from utils import alidayu_tool
from globals import config
import model


class AuthAdminView(AuthView):
    url_rule = '/api/admin_login/'
    view_name = 'auth_admin_api'

    def post(self):
        post = request.form
        tel = post.get("tel")
        recv_code = post.get("recv_code")

        if not tel:
            return success(res={'error_code': 4001, 'msg': '字段缺失'})

        rn = AdminAccount.objects(tel=tel).first()

        if rn:
            key = model.CHECKCODE_KEY.format(tel=tel)
            code = cache.get(key)
            if recv_code == str(code):
                session['account_id'] = rn.id
                return success()
            else:
                print recv_code, str(code)
                return success(res={'error_code': 4001, 'msg': '验证码错误'})

        else:
            return success(res={'error_code': 4002, 'msg': '手机号未注册'})


class CheckCodeAdminView(AuthView):
    url_rule = '/api/check_code_admin/'
    view_name = 'code_admin_api'

    def get(self):
        return bad_request(message='4001')

    def post(self):
        post = request.form
        tel = post.get("tel")
        if not tel:
            return success(res={'r': 1, 'error_code': 4006, 'msg': '手机号不能为空'})

        if not AdminAccount.objects(tel=tel):
            return success(res={'r': 1, 'error_code': 4006, 'msg': '用户不存在'})

        key = model.CHECKCODE_KEY.format(tel=tel)
        code = cache.get(key)
        if not code:
            code = random.randint(100000, 999999)
            cache.incr(key, code)
            cache.expire(key, 300)

        if config.get("DEBUG"):
            print code, "CODEEE"
            ret = True
        else:
            ret = alidayu_tool.send_code(phone=tel, num=str(code))

        if ret:
            return success(res={})
        else:
            return success(res={'error_code': 4001, 'msg': u'验证码发送失败'})


class GetUserView(AuthView):
    url_rule = '/api/dashboard_user/'
    view_name = 'admin_get_user'

    def get(self):
        user_id = session.get("account_id")
        if not user_id:
            return success(res={})
        else:
            rn = AdminAccount.get(id=user_id)
            if rn:
                return success(res={'user': {'name': rn.tel}})
            else:
                return success(res={})


class LoginOutAdminView(AuthView):
    url_rule = '/api/admin_login_out/'
    view_name = 'login_out_api_admin'

    def get(self):
        session.clear()
        return redirect(url_for('dashboard_account'))
