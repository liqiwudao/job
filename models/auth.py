# -*- coding: utf-8 -*-
from datetime import datetime
from mongoengine import (IntField, DateTimeField, StringField, ReferenceField)
from model import BaseModel


# from ext import db


class AuthApi(BaseModel):
    access_key = StringField(max_length=5000, null=False)
    secret_key = StringField(max_length=5000, null=False)
    users = ReferenceField('account')
    meta = {
        'collection': 'auth_api',
        # 'indexes': ['title']
    }
