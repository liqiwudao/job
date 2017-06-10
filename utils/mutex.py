# -*- coding:utf-8 -*-
import time


def simple_mutex_lock(lock_key='_mutex_lock', lock_time=120, max_tries=2, memcached=None):
    """
    一个基于memcached的全局排它锁
    :return:
    :rtype:
    """
    if not memcached:
        return
    _lock = memcached.add(lock_key, 1, lock_time)
    while not _lock and max_tries:
        time.sleep(1)
        _lock = memcached.add(lock_key, 1, lock_time)
        max_tries -= 1
    if not _lock:
        return
    return True


def simple_mutex_release(lock_key='_mutex_lock', memcached=None):
    if memcached:
        memcached.delete(lock_key)
