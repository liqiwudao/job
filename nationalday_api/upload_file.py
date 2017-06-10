#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

import os
import time
import datetime
import json

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
from globals import config
from flask import request, make_response, render_template, abort

from views import BaseApiView
from api.utils import success, failure, bad_request
from utils.qiniu_tool import get_photo
from utils.img import base64_img

import imghdr


# from models.classes import Class

class UploadApiView(BaseApiView):
    url_rule = '/api/upload/'
    view_name = 'upload_api'

    def post(self):
        data = request.form.get("data")
        data = base64_img(data=data)
        now = datetime.datetime.now()
        year, month, day = now.year, now.month, now.day

        img_time = str(time.time())

        try:
            os.mkdir("resume_file/{0}".format(year))
        except OSError, e:
            pass
        try:
            os.mkdir('resume_file/{0}/{1}'.format(year, month))
        except OSError, e:
            pass

        try:
            os.mkdir('resume_file/{0}/{1}/{2}'.format(year, month, day))
        except OSError, e:
            pass

        img_f = os.path.join('resume_file/{0}/{1}/{2}/'.format(year, month, day), img_time)
        with open(img_f, 'wb+') as f:
            f.write(data)
        # ResizeImage(filein=img_f, fileout=out_f, width=1193, height=570, i_type=imgType)
        qiniu_config = config.get("QINIU")
        a_key = qiniu_config.get('access_key')
        s_key = qiniu_config.get("secret_key")
        bucket_name = qiniu_config.get("bucket_name")

        q = Auth(access_key=a_key, secret_key=s_key)
        key = img_f
        token = q.upload_token(bucket_name, key)
        localfile = img_f
        name_url = qiniu_config.get("url")

        ret, info = put_file(token, key, localfile)
        if ret.get("key") == key:
            url = '{0}/{1}'.format(name_url, key)
            # url = get_photo(key=key, size='small')
            return success(res={'url': url, 'file_key': key})
        else:
            return success(res={'error_code': 4001})
