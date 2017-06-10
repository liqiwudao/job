#!/usr/bin/env python
# encoding: UTF-8
from functools import wraps


# copy from douban-utils (https://github.com/douban/douban-utils)
def trans(op):
    def deco(f):
        @wraps(f)
        def _(*a, **kw):
            r = f(*a, **kw)
            if r is not None:
                return op(r)

        return _

    return deco


# copy from douban-utils (https://github.com/douban/douban-utils)
def ptrans(op):
    def deco(f):
        @wraps(f)
        def _(*a, **kw):
            return [op(r) for r in f(*a, **kw)]

        return _

    return deco


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)
