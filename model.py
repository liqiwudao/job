#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'
# coding=utf-8

import ast
from datetime import datetime
import random

from mongoengine import (IntField, DateTimeField, Document, SequenceField, DoesNotExist)
from mongoengine.queryset import DoesNotExist

# from ext import
from libs.rdstore import cache
# from flask import abort
# from mongoengine.base import BaseDocument as Base
# from mongoengine import (
#     Document as BaseDocument, connect, ValidationError, DoesNotExist,
#     QuerySet, MultipleObjectsReturned, IntField, DateTimeField, StringField,
#     SequenceField)
# from mongoengine.queryset.base import BaseQuerySet as BaseQuery

CHECKCODE_KEY = 'nationalday:checkcode:{tel}'
SEARCH_KEY = 'nationalday:search:{type}:{id}'
OBJ_KEY = 'nationalday:object:{coll_name}:{id}'

SAMPLE_SIZE = 200
TOTAL_SIZE = 2000
ARTICLE_KEY = 'nationalday:content:{id}'
TIMEOUT = 60 * 60


class BaseModel(Document):
    id = SequenceField(primary_key=True)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    state = IntField(null=False, default=100)

    meta = {'allow_inheritance': True,
            'abstract': True,
            'strict': False
            }

    @classmethod
    def pagination(cls, page, limit, rn):
        if not rn:
            count = 0
            page_num = page
            data = []
        else:
            skip = 0 if page == 1 else (page - 1) * limit
            end = skip + limit
            count = rn.count()
            page_num, remainder = divmod(count, limit)
            page_num = page_num if remainder == 0 else (page_num + 1)
            data = rn[skip: end]

        data = {
            'data': data,
            'count': count,
            'page_num': page_num,
            'current': page,
        }

        return data

    @classmethod
    def get(cls, id):
        coll_name = cls._meta['collection']
        key = OBJ_KEY.format(coll_name=coll_name, id=id)
        rs = cache.get(key)
        if rs:
            return cls.from_json(rs)
        try:
            rs = cls.objects.get(id=id)
        except DoesNotExist, e:
            return False
        cache.set(key, rs.to_json())
        return rs

    @classmethod
    def find_one(cls, **kwargs):
        count = cls.objects(**kwargs).all().count()
        return cls.objects.all()[random.randint(0, count - 1)]

    @classmethod
    def get_all_data(cls, **kwargs):
        rn = cls.objects(kwargs).all()
        return rn

    @classmethod
    def get_multi(cls, ids):
        return [cls.get(i) for i in ids if i]

    @classmethod
    def create(cls, **kwargs):
        coll_name = cls._meta['collection']
        model = cls(**kwargs)
        model.save()
        key = OBJ_KEY.format(coll_name=coll_name, id=id)
        cache.set(key, model.to_json())
        return model

    @classmethod
    def get_or_create(cls, **kwargs):
        try:
            return cls.objects.get(id=kwargs['id'])
        except DoesNotExist:
            kwargs.update({'update_at': datetime.now()})
            model = cls(**kwargs)
            model.save()
            return model

    @classmethod
    def update_doc(cls, id, **kwargs):
        rn = cls.objects(id=id).update(upsert=True, **kwargs)
        if not rn:
            return False
        else:
            rn = cls.objects(id=id).first()
        coll_name = cls._meta['collection']
        key = OBJ_KEY.format(coll_name=coll_name, id=id)
        cache.set(key, rn.to_json())
        return rn

    @classmethod
    def get_sample_ids(cls, size):
        samples = list(cls.objects.aggregate(
            {'$sample': {'size': size}}))
        return [s['_id'] for s in samples]


def search(subject_id, type):
    key = SEARCH_KEY.format(id=subject_id, type=type)

    if not subject_id:
        return []
    comment_ids = cache.lrange(key, 0, -1)
    # if comment_ids:
    #     return Comment.get_multi(comment_ids)
    # songs = []
    # if type == 'artist':
    #     artist = Artist.get(id=subject_id)
    #     songs.extend(Song.objects(artist=artist))
    # else:
    #     songs.extend(Song.get(id=subject_id))
    #
    # comments = sum([list(Comment.objects(song=song)) for song in songs], [])
    #
    # comment_ids = [comment.id for comment in comments]
    # if comment_ids:
    #     cache.rpush(key, *comment_ids)
    # return comments

# class BaseQuerySet(QuerySet):
#     def get_or_404(self, *args, **kwargs):
#         try:
#             return self.get(*args, **kwargs)
#         except (MultipleObjectsReturned, DoesNotExist, ValidationError):
#             abort(404)
#
#     def objects(self, *args, **kwargs):
#         super(BaseQuery, self).__init__(*args, **kwargs)
#
# class Document(BaseDocument):
#     meta = {'abstract': True,
#             'queryset_class': BaseQuerySet}
#
#     # def __init__(self):
#     #     pass
#
#
#     def insert(self, *args, **kwargs):
#         super(BaseDocument, self).__init__(*args, **kwargs)
#         self.save()
#         return self


# def select(self, *args, **kwargs):
#     super(Base, self).__init__()
#     b = self.objects.get(**kwargs)
#     print b
#     return b

# class TTTT(BaseDocument):
