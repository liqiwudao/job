#!/usr/bin/env python
# -*- coding: utf-8
import json

__author__ = 'zjw'

from flask import request, abort, render_template, session, redirect, url_for

from log import app_logger
from globals import config
import random

from views import BaseView, LoginView
from models.resume import Resume
from models.account import Account

from models.job import Job
from models.box import Box
from constants import EXPERIENCE, CATEGORY, JOB_CLASS, LEVEL

from utils.qiniu_tool import get_photo
import constants


class HomeView(BaseView):
    url_rule = '/'
    view_name = 'home'

    def get(self, **kwargs):
        return render_template('%s/index/index.html' % (self.template_base), msg=kwargs.get("msg"))


class CandidatesView(BaseView):
    url_rule = '/candidates/'
    view_name = 'candidates'

    def get(self, **kwargs):
        return render_template('%s/index/candidates.html' % (self.template_base), msg=kwargs.get("msg"))


class JobDetailView(BaseView):
    url_rule = '/job/'
    view_name = 'job_detail'

    def get(self, **kwargs):
        job_id = request.args.get("job_id")
        if not job_id:
            return abort(404)

        rn = Job.get(id=job_id)
        if not rn:
            return abort(404)
        else:

            box_rn = Box.objects(state=100, jobs=int(job_id), accounts=Account.get(id=session.get("user_id"))).first()

            if not box_rn:
                post_flag = True
            else:
                post_flag = False

            data = {
                'post_flag': post_flag,
                'id': rn.id,
                'name': rn.name,
                'department': rn.department,
                'category': CATEGORY.get(rn.category),
                'experience': EXPERIENCE.get(rn.experience),
                'education': LEVEL.get(rn.education),
                'salary': "{0}-{1}k".format(rn.salary_start, rn.salary_end),
                'location': rn.location,
                'description': rn.description,
                'temptation': rn.temptation,
                'time': rn.created_at.strftime("%Y-%m-%d"),
                'classes': JOB_CLASS.get(rn.classes)
            }

        return render_template('%s/index/jobdetail.html' % (self.template_base), msg=kwargs.get("msg"), data=data)


class DropBoxlView(BaseView):
    url_rule = '/user/drop_box/'
    view_name = 'drop_box'

    def get(self, **kwargs):
        return render_template('%s/index/dropbox.html' % (self.template_base), msg=kwargs.get("msg"))


class BlogDetailView(BaseView):
    url_rule = '/blog/'
    view_name = 'blog_detail'

    def get(self, **kwargs):
        return render_template('%s/index/blogdetail.html' % (self.template_base), msg=kwargs.get("msg"))


class BlogPageView(BaseView):
    url_rule = '/blog_page/'
    view_name = 'blog_page'

    def get(self, **kwargs):
        return render_template('%s/index/blog_page.html' % (self.template_base), msg=kwargs.get("msg"))


class ResumeCheckView(BaseView):
    url_rule = '/resume_check/'
    view_name = 'resume_check_page'

    def get(self, **kwargs):

        account = Account.get(id=session.get("user_id"))
        rn = Resume.objects(accounts=account).first()
        if rn:
            return redirect(url_for('resume_view'))

        else:
            return render_template('%s/index/resumecheck.html' % (self.template_base), msg=kwargs.get("msg"))


class ResumeEditView(BaseView):
    url_rule = '/resume_view/'
    view_name = 'resume_view'

    def get(self, **kwargs):
        account = Account.get(id=session.get("user_id"))
        rn = Resume.objects(accounts=account).first()
        if not rn:
            return redirect(url_for('resume_check_page'))
        education = []
        for edu in rn.education:
            level = edu.get("level", "")
            if level:
                level = constants.LEVEL.get(level)
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

            'file_url': file_url,
            'filename': filename
        }
        return render_template('%s/index/my_resume.html' % (self.template_base), msg=kwargs.get("msg"), resume=data)


class ResumeView(BaseView):
    url_rule = '/user/resume_edit/'
    view_name = 'resume_edit'

    def get(self, **kwargs):
        account = Account.get(id=session.get("user_id"))
        rn = Resume.objects(accounts=account).first()
        if not rn:
            return render_template('%s/index/resume.html' % (self.template_base), msg=kwargs.get("msg"), resume='')
        else:
            education = []
            for edu in rn.education:
                level = edu.get("level", "")
                if level:
                    level = constants.LEVEL.get(level)
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

            # file_url = rn.file_key
            filename = rn.file_name
            expect_job = rn.expect_job
            expect_salary = rn.expect_salary
            postscript = rn.postscript
            # temptation = rn.temptation

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
                # 'temptation': temptation,

                # 'file_url': file_url,
                'filename': filename
            }
            data = json.dumps(data)
            return render_template('%s/index/resume.html' % (self.template_base), msg=kwargs.get("msg"),
                                   resume=data)
