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

from models.job import Job
from models.admin import AdminAccount

from constants import JOB_CLASS, LEVEL, EXPERIENCE, CATEGORY


class JobApiView(BaseApiView):
    url_rule = '/api/job/'
    view_name = 'job_api'

    def get(self):
        args = request.args
        job_class = args.get("job_class")
        page = int(args.get("page"))
        limit = int(args.get("limit"))
        option = args.get("option")

        job_list = []
        if option == 'all':
            if not job_class or job_class == '0':
                rn = Job.objects().all()
            else:
                rn = Job.objects(classes=int(job_class)).all()
            obj = Job.pagination(page=page, limit=limit, rn=rn)
            for job in obj.get("data"):
                create_time = job.created_at.strftime("%Y-%m-%d %H:%M:%S")
                job_list.append(
                    {"name": job.name, 'department': job.department, 'time': create_time,
                     'classes': JOB_CLASS.get(job.classes), 'location': job.location,
                     'id': job.id})
        else:
            experience = args.get("experience")
            category = args.get("category")
            data = {
                'state': 100
            }
            if job_class and job_class != '0':
                data['classes'] = int(job_class)

            if experience and experience != '0':
                data['experience'] = int(experience)

            if category and category != '0':
                data['category'] = int(category)

            rn = Job.objects(**data).all()
            obj = Job.pagination(page=page, limit=limit, rn=rn)
            for job in obj.get("data"):
                create_time = job.created_at.strftime("%Y-%m-%d")
                job_list.append(
                    {
                        "name": job.name,
                        'time': create_time,
                        'department': job.department,
                        'classes': JOB_CLASS.get(job.classes),
                        'location': job.location,
                        'salary': "{0}-{1}k".format(job.salary_start, job.salary_end),
                        'experience': EXPERIENCE.get(job.experience),
                        'education': LEVEL.get(job.education),
                        'temptation': job.temptation,
                        'id': job.id
                    }
                )

        obj['data'] = job_list

        return success(res={'data': job_list})

    def post(self):
        account = AdminAccount.get(id=session.get("account_id"))
        if not account:
            return success(res={"error_code": 4001, 'msg': '请登入'})

        post = request.form
        job_class = post.get("job_class")
        job_name = post.get("job_name")
        job_department = post.get('job_department')
        job_category = post.get("job_category")
        job_experience = post.get("job_experience")
        education = post.get("education")
        salary_start = post.get("salary_start")
        salary_end = post.get("salary_end")
        location = post.get("location")
        description = post.get("description")
        temptation = post.get("temptation")
        option = post.get("option")

        if (not job_class) or (not job_name) or (not job_department) or (not job_category) or (not job_experience) or (
                not education) or (not description) or (not location) or (not temptation):
            return success(res={"error_code": 4001, 'msg': '字段缺失'})

        data = {
            'name': job_name,
            'accounts': account,
            'department': job_department,
            'category': int(job_category),
            'experience': int(job_experience),
            'education': int(education),
            'salary_start': int(salary_start),
            'salary_end': int(salary_end),
            'location': location,
            'description': description,
            'classes': int(job_class),
            'temptation': temptation,
        }

        if option == 'update':
            job_id = post.get("job_id")
            rn = Job.update_doc(id=job_id, **data)
        else:
            rn = Job.create(**data)

        if rn:
            return success(res={'id': rn.id})
        else:
            return success(res={'error_code': 4001, 'msg': u'保存失败'})
