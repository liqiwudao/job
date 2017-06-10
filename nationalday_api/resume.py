#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

from flask import request, make_response, render_template, abort, session
from views import BaseApiView
import json
from api.utils import success, failure, bad_request
from globals import config

from utils.qiniu_tool import get_photo
from utils import convert

from models.resume import Resume
from models.account import Account


class ResumeApiView(BaseApiView):
    url_rule = '/api/resume/'
    view_name = 'resume_api'

    def post(self):
        account = Account.get(id=session.get("user_id"))
        if not account:
            return success(res={"error_code": 4001, 'msg': '请登入'})

        post = request.form
        name = post.get("name")
        tel = post.get("tel")
        sex = post.get('sex')
        email = post.get("email")
        birthday = post.get("birthday")

        if (not name) or (not tel) or (not sex) or (not email):
            return success(res={"error_code": 4001, 'msg': '字段缺失'})


        school = post.get("school", '')
        major = post.get("major", '')
        level = int(post.get("level", 2))
        graduation_date = post.get("graduation_date", '')

        company = post.get("company", '')
        job = post.get("job", '')
        job_date_start = post.get("job_date_start", '')
        job_date_end = post.get("job_date_end", '')
        job_content = post.get("job_content", '')

        expect_job = post.get("expect_job", '')
        expect_salary = post.get("expect_salary")
        if expect_salary:
            expect_salary = int(expect_salary)
        else:
            expect_salary = 0
        postscript = post.get("postscript", '')

        description = post.get("description", '')
        file_key = post.get("file_key", '')
        filename = post.get("filename", '')

        data = {
            'name': name,
            'tel': tel,
            'sex': sex,
            'accounts': account,
            'email': email,
            'birthday': birthday,

            'education': [
                {
                    'school': school,
                    'major': major,
                    'level': level,
                    'graduation_date': graduation_date
                }
            ],
            'experience': [
                {
                    'company': company,
                    'job': job,
                    'job_date_start': job_date_start,
                    'job_date_end': job_date_end,
                    'job_content': job_content
                }
            ],
            'expect_job': expect_job,
            'expect_salary': expect_salary,
            'postscript': postscript,
            'description': description,
            'file_key': file_key,
            'file_name': filename,
        }

        obj = Resume.objects(accounts=account).first()
        if obj:
            rn = Resume.update_doc(obj.id, **data)
        else:
            rn = Resume.create(**data)
        if rn:
            return success(res={})
        else:
            return success(res={'error_code': 4001, 'msg': u'保存失败'})
