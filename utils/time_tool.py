# -*- coding:utf-8 -*-
import arrow
from functools import partial
import time
import datetime


def comment_time(now, date):
    difference = int((now - date).total_seconds())
    if difference < 3600:
        r_time, remainder, = divmod(difference, 60)
        r_time = r_time if not remainder else r_time + 1
        r_time = u"%s 分钟前" % (r_time)
    elif difference >= 3600 and difference < 86400:
        r_time, remainder, = divmod(difference, 3600)
        r_time = r_time if not remainder else r_time + 1
        r_time = u"%s 小时前" % (r_time)
    elif difference >= 86400 and difference < 2592000:
        r_time, remainder, = divmod(difference, 86400)
        r_time = r_time if not remainder else r_time + 1
        r_time = u"%s 天前" % (r_time)
    elif difference >= 2592000 and difference < 31536000:
        r_time, remainder, = divmod(difference, 2592000)
        r_time = r_time if not remainder else r_time + 1
        r_time = u"%s 月前" % (r_time)
    elif difference >= 31536000:
        r_time, remainder, = divmod(difference, 31536000)
        r_time = r_time if not remainder else r_time + 1
        r_time = u"%s 年前" % (r_time)

    return r_time


now = arrow.now

utcnow = arrow.utcnow

prc_tz = 'PRC'  # MUST uppercase!


def prcnow():
    return utcnow().to(prc_tz)


def prctoday():
    return prcnow().date()


def span_range(start, end, frame, tz=None):
    return arrow.Arrow.span_range(frame, start, end, tz=tz)


def time_range(start, end, frame, tz=None):
    return arrow.Arrow.range(frame, start, end, tz=tz)


span_range_by_minute = partial(span_range, frame='minute')
span_range_by_hour = partial(span_range, frame='hour')
span_range_by_day = partial(span_range, frame='day')

prc_span_range_by_minute = partial(span_range, frame='minute', tz=prc_tz)
prc_span_range_by_hour = partial(span_range, frame='hour', tz=prc_tz)
prc_span_range_by_day = partial(span_range, frame='day', tz=prc_tz)

prc_range_by_minute = partial(time_range, frame='minute', tz=prc_tz)
prc_range_by_hour = partial(time_range, frame='hour', tz=prc_tz)
prc_range_by_day = partial(time_range, frame='day', tz=prc_tz)


def utc_today_int():
    return int(arrow.utcnow().format('YYYYMMDD'))


def prc_today_int():
    return int(prcnow().format('YYYYMMDD'))


def utc_from_today_int(date_int):
    return arrow.Arrow.strptime(str(date_int), '%Y%m%d')


def prc_from_today_int(date_int):
    return arrow.Arrow.strptime(str(date_int), '%Y%m%d', tzinfo=prc_tz)


def timestamp(is_float=False):
    if is_float:
        return arrow.utcnow().float_timestamp
    else:
        return arrow.utcnow().timestamp


def utc_from_timestamp(ts):
    return arrow.Arrow.utcfromtimestamp(ts)


def prc_from_timestamp(ts):
    return arrow.Arrow.fromtimestamp(ts, prc_tz)

