#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

from flask import request, make_response, render_template, abort
from views import BaseApiView
import json
from api.utils import success, failure, bad_request




class ApplyApiView(BaseApiView):
    url_rule = '/api/apply/'
    view_name = 'apply_api'

    def post(self):
        post = request.form
        song_id = post.get("job_id")
        name = post.get("name")
        if not song_id and not name:
            return bad_request(message=u'参数缺失')

        if not name or not song_id:
            return bad_request(message=u'参数缺失')
        else:
            try:
                song_id = int(song_id)
            except ValueError:
                return bad_request(message=u'id错误')

        data = {
            'song_id': song_id,
            'state': 100,
            'name': name
        }

        rn = Song.create(**data)

        if not rn:
            return bad_request(message='4001')
        else:
            return success(res={'msg': 'ok'})
