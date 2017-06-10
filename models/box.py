# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import (IntField, StringField, ReferenceField)
from model import BaseModel


# from ext import db

# state 100投递成功 200不合适 300待面试

class Box(BaseModel):
    accounts = ReferenceField('Account', null=False)
    jobs = ReferenceField('Job', null=False)
    resumes = ReferenceField('Resume', null=False)
    drop_state = IntField(null=False)

    meta = {
        'collection': 'box',
        # 'indexes': ['title']
    }
