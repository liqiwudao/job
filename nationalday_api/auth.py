#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'zjw'

import random
from flask import request, session
from views import AuthView
# import json
import hmac
from api.utils import success, bad_request
from libs.rdstore import cache
# from models.auth import AuthApi
from models.account import Account
from utils import alidayu_tool
from globals import config
import model


class AuthApiView(AuthView):
    url_rule = '/api/login/'
    view_name = 'auth_api'

    def post(self):
        post = request.form
        tel = post.get("tel")
        passwd = post.get('passwd')

        if not tel or not passwd:
            return success(res={'error_code': 4001, 'msg': '字段缺失'})

        if len(passwd) < 6:
            return success(res={'error_code': 4001, 'msg': "密码格式错误"})

        rn = Account.objects(tel=tel).first()

        if rn:
            passwd = str(passwd)
            hash_passwd = hmac.new(passwd)
            hash_passwd.update(passwd[1:5])

            if hash_passwd.hexdigest() == rn.password:
                session['user_id'] = rn.id
                return success()
            else:
                return success(res={'error_code': 4001, 'msg': '密码错误'})

        else:
            return success(res={'error_code': 4002, 'msg': '手机号未注册'})


class CheckCodeView(AuthView):
    url_rule = '/api/check_code/'
    view_name = 'code_api'

    def get(self):
        return bad_request(message='4001')

    def post(self):
        post = request.form
        tel = post.get("tel")
        if not tel:
            return success(res={'r': 1, 'error_code': 4006, 'msg': '手机号不能为空'})

        if Account.objects(tel=tel):
            return success(res={'r': 1, 'error_code': 4006, 'msg': '手机已注册'})

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


class ChangePasswdView(AuthView):
    url_rule = '/api/change_passwd/'
    view_name = 'change_passwd_api'

    def post(self):
        post = request.form
        tel = post.get("tel")
        passwd = post.get("passwd")

        if len(passwd) < 6:
            return success(res={'error_code': 4001, 'msg': '密码不得小于6位'})

        rn = Account.objects(tel=tel).first()
        if not rn:
            return success(res={'error_code': 4001, 'msg': '用户不存在'})
        passwd = str(passwd)
        hash_passwd = hmac.new(passwd)
        hash_passwd.update(passwd[1:5])
        data = {'password': hash_passwd.hexdigest()}
        obj = Account.update_doc(id=rn.id, **data)
        return success(res={'user_id': obj.id, 'msg': '用户不存在'})


class RegisterView(AuthView):
    url_rule = '/api/register/'
    view_name = 'register_api'

    def post(self):
        post = request.form
        tel = post.get("tel")
        name = post.get('name')
        code = post.get('code')
        passwd = post.get('passwd')

        if not code or not name or not passwd:
            return success(res={'error_code': 4001})

        if Account.objects(tel=tel):
            return success(res={'error_code': 4001, 'msg': '手机已注册'})

        if len(passwd) < 6:
            return success(res={'error_code': 4001})

        key = model.CHECKCODE_KEY.format(tel=tel)

        passwd = str(passwd)
        hash_passwd = hmac.new(passwd)
        hash_passwd.update(passwd[1:5])

        if code == cache.get(key):
            img_key = post.get('img_key')
            if not img_key:
                img_key = 'head.jpg'
            data = {'tel': tel, 'name': name, 'password': hash_passwd.hexdigest(), 'state': 100,
                    'head_img_key': img_key}
            rn = Account.create(**data)
        else:
            return success(res={'error_code': 4001, 'msg': '验证码错误'})

        if not rn:
            return success(res={'error_code': 4001})
        else:
            session['user_id'] = rn.id
            return success()


class LoginOutView(AuthView):
    url_rule = '/api/login_out/'
    view_name = 'login_out_api'

    def post(self):
        session.clear()
        return success()
