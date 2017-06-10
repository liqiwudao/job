#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

import os
import time
import datetime
import json

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from globals import config
from flask import request, make_response, render_template, abort, session, send_file

from views import BaseApiView
from models.account import Account
from models.resume import Resume
from api.utils import success, failure, bad_request
from utils.qiniu_tool import get_photo
from utils.img import base64_img

import imghdr


# from models.classes import Class

class UploadApiView(BaseApiView):
    url_rule = '/api/download_resume/'
    view_name = 'download_api'

    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            if not session.get("account_id"):
                return success(res={'error_code': 4001, 'msg': '未登入'})
            else:
                user_id = request.args.get("user_id")

        obj = Account.get(id=user_id)

        if obj:
            rn = Resume.objects(accounts=obj).first()
            if not rn:
                return success(res={'error_code': 4001, 'msg': '下载失败'})

            file_key = rn.file_key
            if file_key:
                response = make_response(send_file(file_key))
                response.headers["Content-Disposition"] = "attachment; filename={0};".format(rn.file_name)
                return response
            else:
                return success(res={'error_code': 4001, 'msg': '下载失败'})
        else:
            return success(res={'error_code': 4001, 'msg': '下载失败'})
