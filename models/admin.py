# -*- coding:utf-8 -*-
from mongoengine import (IntField, DateTimeField, StringField, ReferenceField, DictField)
from model import BaseModel


# from ext import db

class AdminAccount(BaseModel):
    tel = IntField(null=False)
    meta = {'collection': 'admin_account'}
