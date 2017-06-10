# -*- coding:utf-8 -*-

import json

import functools
from flask import request, redirect, session, url_for
from models.auth import AuthApi
from models.account import Account

# from utils.auth import NationaldayAuth
from api.utils import success, failure, bad_request


def backup_auth(f):
    @functools.wraps(f)
    def _f(*args, **kwargs):
        user_id = session.get("account_id")
        if not user_id:
            return redirect(url_for('dashboard_account'))

        return f(*args, **kwargs)

    return _f


def require_login(f):
    @functools.wraps(f)
    def _f(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            msg = json.dumps({})
        else:
            rn = Account.get(id=user_id)
            if not rn:
                msg = {}
            else:
                msg = {'name': rn.name, 'id': user_id}

        if isinstance(kwargs, dict):
            pass
        else:
            kwargs = {}
        kwargs.update({'msg': json.dumps(msg)})
        return f(*args, **kwargs)

    return _f


def auth_login(f):
    @functools.wraps(f)
    def _f(*args, **kwargs):
        user_id = session.get("user_id")
        if not user_id:
            return redirect(url_for('login', redirect=request.url))
        else:
            rn = Account.get(id=user_id)
            if not rn:
                msg = {}
            else:
                msg = {'name': rn.name, 'id': user_id}

        if isinstance(kwargs, dict):
            pass
        else:
            kwargs = {}
        kwargs.update({'msg': json.dumps(msg)})
        return f(*args, **kwargs)

    return _f

#
# def api_auth(f):
#     @functools.wraps(f)
#     def _f(*args, **kwargs):
#         post = request.form
#         data = post.get('data')
#         try:
#             data = json.loads(data)
#         except Exception:
#             return bad_request(message=4001)
#
#         access_key = data.get('access_key')
#         if not access_key:
#             return bad_request(message=4001)
#
#         obj = AuthApi.objects.filter({'access_key': access_key})
#         if not obj:
#             return bad_request(message=4001)
#         else:
#             secret_key = obj.secret_key
#
#         if not NationaldayAuth(access_key=access_key, secret_key=secret_key).auth_msg(**data):
#             return bad_request(message=4001)
#
#         return f(*args, **kwargs)
#
#     return _f
