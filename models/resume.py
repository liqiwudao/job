# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import (IntField, StringField, ReferenceField, EmailField, ListField)
from model import BaseModel


# from ext import db


class Resume(BaseModel):
    name = StringField(max_length=5000, null=False)
    accounts = ReferenceField('Account', null=False)
    tel = StringField(max_length=5000, null=False)
    sex = IntField(null=False)
    birthday = StringField(max_length=5000, null=False)

    email = EmailField(null=False)

    education = ListField(null=True)

    experience = ListField(null=True)

    expect_job = StringField(max_length=5000, null=True)
    expect_salary = IntField(null=True)

    postscript = StringField(max_length=5000, null=True)

    description = StringField(max_length=50000, null=True)

    file_key = StringField(max_length=1000, null=True)
    file_name = StringField(max_length=5000, null=True)

    meta = {
        'collection': 'resume',
        # 'indexes': ['title']
    }
