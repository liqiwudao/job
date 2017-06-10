#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

import json
from flask import request, abort, render_template, session

from views import BackUpView

from models.job import Job
from models.account import Account
from models.resume import Resume
from models.box import Box
from constants import EXPERIENCE, CATEGORY, JOB_CLASS, LEVEL


# from models.content import Content
# from models.tag import Tag


class HomeView(BackUpView):
    url_rule = '/dashboard/'
    view_name = 'dashboard_index'

    def get(self):
        return render_template('%s/index/index.html' % self.template_base)
        # return render_template('base.html')


class ResumeAdminView(BackUpView):
    url_rule = '/dashboard/resume/'
    view_name = 'dashboard_resume'

    def get(self):
        return render_template('%s/index/resume_list.html' % self.template_base)


class JobAdminView(BackUpView):
    url_rule = '/dashboard/job/'
    view_name = 'dashboard_job'

    def get(self):
        return render_template('%s/index/job_list.html' % self.template_base)


class PublishJobView(BackUpView):
    url_rule = '/dashboard/publish_job/'
    view_name = 'publish_job'

    def get(self):
        return render_template('%s/index/publish_job.html' % self.template_base)


class EditJobView(BackUpView):
    url_rule = '/dashboard/edit_job/'
    view_name = 'edit_job'

    def get(self):
        job_id = request.args.get("job_id")
        if not job_id:
            return abort(404)

        rn = Job.get(id=job_id)
        if not rn:
            return abort(404)

        data = {
            'id': rn.id,
            'name': rn.name,
            'department': rn.department,
            'category': rn.category,
            'experience': rn.experience,
            'education': rn.education,
            'salary_start': rn.salary_start,
            'salary_end': rn.salary_end,
            'location': rn.location,
            'description': rn.description,
            'temptation': rn.temptation,
            'classes': rn.classes
        }

        return render_template('%s/index/edit_job.html' % self.template_base, data=json.dumps(data))


class ResumeDetailView(BackUpView):
    url_rule = '/dashboard/resume_detail/'
    view_name = 'dashboard_resume_detail'

    def get(self, **kwargs):
        box_id = request.args.get("box_id")
        box_rn = Box.get(id=box_id)
        rn = Resume.get(id=box_rn.resumes.id)
        education = []
        for edu in rn.education:
            level = edu.get("level", "")
            if level:
                level = LEVEL.get(level)
            education.append({
                "school": edu.get("school", ''),
                "major": edu.get("major", ""),
                'level': level,
                'graduation_date': edu.get("graduation_date", '')
            })

        experience = []
        for exp in rn.experience:
            experience.append({
                "company": exp.get("company", ''),
                "job": exp.get("job", ''),
                "job_content": exp.get("job_content", ''),
                "job_date_start": exp.get('job_date_start', ''),
                "job_date_end": exp.get('job_date_end', ''),
            })

        file_url = rn.file_key
        filename = rn.file_name
        expect_job = rn.expect_job
        expect_salary = rn.expect_salary
        postscript = rn.postscript
        description = rn.description

        data = {
            'name': rn.name,
            'birthday': rn.birthday,
            'sex': rn.sex,
            'tel_num': rn.tel,
            'email': rn.email,
            'education': education,
            'experience': experience,
            'expect_job': expect_job,
            'expect_salary': expect_salary,
            'postscript': postscript,
            'description': description,
            'box_id': box_id,
            'drop_state': box_rn.drop_state,

            'user_id': rn.accounts.id,
            'file_url': file_url,
            'filename': filename
        }
        print data,"AAAA"
        return render_template('%s/index/resume.html' % (self.template_base), msg=kwargs.get("msg"), data=data)


class JobDetailView(BackUpView):
    url_rule = '/dashboard/job_detail/'
    view_name = 'detail_job'

    def get(self):
        job_id = request.args.get("job_id")
        if not job_id:
            return abort(404)

        rn = Job.get(id=job_id)
        if not rn:
            return abort(404)
        else:
            data = {
                'id': rn.id,
                'name': rn.name,
                'department': rn.department,
                'category': CATEGORY.get(rn.category),
                'experience': EXPERIENCE.get(rn.experience),
                'education': rn.education,
                'salary_start': rn.salary_start,
                'salary_end': rn.salary_end,
                'location': rn.location,
                'description': rn.description,
                'temptation': rn.temptation,
                'classes': JOB_CLASS.get(rn.classes)
            }

        return render_template('%s/index/job_detail.html' % self.template_base, data=data)
