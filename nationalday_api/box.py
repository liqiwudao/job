#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

from flask import request, make_response, render_template, abort, session
from views import BaseApiView
import json
from api.utils import success, failure, bad_request

from models.box import Box
from models.job import Job
from models.account import Account
from models.resume import Resume

from constants import JOB_CLASS, LEVEL, EXPERIENCE, CATEGORY


class BoxApiView(BaseApiView):
    url_rule = '/api/box/'
    view_name = 'box_api'

    def get(self):
        args = request.args
        page = int(args.get("page"))
        limit = int(args.get("limit"))
        option = args.get("option")
        drop_state = int(args.get("drop_state"))

        job_list = []
        if option == 'all':
            # if not job_class and job_class == '0':
            data = {}
            if drop_state:
                data = {
                    'drop_state': drop_state,
                }

            box_rn = Box.objects(**data).all()
            obj = Job.pagination(page=page, limit=limit, rn=box_rn)
            for box in obj.get("data"):
                job = Job.get(id=box.jobs.id)
                resume = Resume.get(id=box.resumes.id)
                if not job:
                    continue

                create_time = box.created_at.strftime("%Y-%m-%d")
                job_list.append(
                    {
                        "drop_state": box.drop_state,
                        "name": job.name,
                        'time': create_time,
                        'department': job.department,
                        'classes': JOB_CLASS.get(job.classes),
                        'resume_name': resume.name,
                        'tel': resume.tel,
                        'resume_id': resume.id,
                        'drop_state': box.drop_state,
                        'box_id': box.id,
                        # 'location': job.location,
                        # 'salary': "{0}-{1}k".format(job.salary_start, job.salary_end),
                        # 'experience': EXPERIENCE.get(job.experience),
                        # 'education': LEVEL.get(job.education),
                        # 'temptation': job.temptation,
                        'id': job.id
                    }
                )
        else:
            data = {
                'state': 100,
                'accounts': session.get("user_id")
            }

            if drop_state:
                data['drop_state'] = int(drop_state)

            box_rn = Box.objects(**data).all()
            obj = Job.pagination(page=page, limit=limit, rn=box_rn)
            for box in obj.get("data"):
                job = Job.get(id=box.jobs.id)
                if not job:
                    continue

                create_time = job.created_at.strftime("%Y-%m-%d")
                job_list.append(
                    {
                        "drop_state": box.drop_state,
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
        post = request.form
        job_id = post.get("job_id")
        option = post.get("option")

        if option == "update":
            box_id = post.get("box_id")
            drop_state = post.get("drop_state")
            data = {
                'drop_state': int(drop_state)
            }
            rn = Box.update_doc(id=box_id, **data)
        else:
            if not job_id:
                return success(res={"error_code": 4001, 'msg': '参数错误'})
            count = len(Box.objects(state=100, accounts=session.get("user_id")))
            if count > 2:
                return success(res={'error_code': 4001, 'msg': '已投递3份简历，到达上限！'})

            resume_rn = Resume.objects(state=100, accounts=session.get("user_id")).first()

            if not resume_rn:
                return success(res={'error_code': 4004, 'msg': '暂无简历，确认创建简历?'})

            data = {
                "jobs": Job.get(id=job_id),
                'drop_state': 100,
                "accounts": Account.get(id=session.get("user_id")),
                'resumes': resume_rn.id
            }

            rn = Box.create(**data)

        if not rn:
            return success(res={'error_code': 4001, 'msg': '投递失败'})

        return success(res={'id': rn.id})
