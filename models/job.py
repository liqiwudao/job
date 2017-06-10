# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import (IntField, StringField, ReferenceField)
from model import BaseModel


# from ext import db


class Job(BaseModel):
    name = StringField(max_length=5000, null=False)
    accounts = ReferenceField('AdminAccount', null=False)
    department = StringField(max_length=5000, null=False)
    category = IntField(null=False)
    experience = IntField(null=False)
    education = IntField(null=False)
    salary_start = IntField(null=False)
    salary_end = IntField(null=False)
    location = StringField(max_length=5000, null=False)
    description = StringField(max_length=50000, null=False)
    temptation = StringField(max_length=5000, null=False)
    classes = IntField(null=False)

    meta = {
        'collection': 'job',
        # 'indexes': ['title']
    }
