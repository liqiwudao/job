# -*- coding:utf-8 -*-
from mongoengine import (IntField, DateTimeField, StringField, ReferenceField, DictField)
from model import BaseModel


# from ext import db

class Account(BaseModel):
    name = StringField(max_length=5000, null=False)
    tel = IntField(null=False)
    password = StringField(max_length=5000, null=False)
    head_img_key = StringField(max_length=5000, null=False)
    meta = {'collection': 'account'}
