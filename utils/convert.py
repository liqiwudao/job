#-*- coding:utf-8 -*-
from bson import ObjectId
from bson.errors import InvalidId


def to_float(v, default=0.0):
    try:
        v = float(v)
    except (ValueError, TypeError):
        v = default
    return v


def to_int(v, default=0):
    try:
        v = int(v)
    except (ValueError, TypeError):
        v = default
    return v


def to_long(v, default=0):
    try:
        v = long(v)
    except (ValueError, TypeError):
        v = default
    return v


def to_object_id(o, default=None):
    if not o:
        return default
    try:
        v = ObjectId(o)
    except (InvalidId, ValueError, TypeError):
        v = default
    return v


def to_unicode(s):
    """ Convert to unicode, raise exception with instructive error
    message if s is not unicode, ascii, or utf-8. """
    if not isinstance(s, unicode):
        if not isinstance(s, str):
            raise TypeError('You are required to pass either unicode or string here, not: %r (%s)' % (type(s), s))
        try:
            s = s.decode('utf-8')
        except UnicodeDecodeError, le:
            raise TypeError('You are required to pass either a unicode object or a utf-8 string here.'
                            'You passed a Python string object which contained non-utf-8: %r.'
                            ' The UnicodeDecodeError that resulted from attempting to interpret it as utf-8 was: %s'
                            % (s, le,))
    return s


def to_utf8(s):
    return to_unicode(s).encode('utf-8')


def to_unicode_if_string(s):
    if isinstance(s, basestring):
        return to_unicode(s)
    else:
        return s


def to_utf8_if_string(s):
    if isinstance(s, basestring):
        return to_utf8(s)
    else:
        return s


def to_bool(s, default=False):
    if not s:
        return False
    if s in ('', u''):
        return False
    s = s.lower()
    if s in (u'on', u'true', u'1', 'on', 'true', '1'):
        return True
    if s in (u'off', u'false', u'0', 'off', 'false', '0'):
        return False
    return default


def convert_by_type_name(val, type_name):
    map_funs = {
        u'INT': to_int,
        u'BOOL': to_bool,
        u'LONG': to_long,
        u'OID': to_object_id,
        u'FLOAT': to_float,
        u'UNICODE': to_unicode,
        u'UTF8': to_utf8,
    }
    fun = map_funs.get(type_name.upper())
    if not fun:
        return val
    if isinstance(val, list):
        return map(fun, val)
    return fun(val)


def round_currency(float_val):
    return round(float_val, 2)


def round_money_cent(float_val, subunit=100):
    return int(round(float_val * subunit, 0))


def round_money_int(float_val):
    return int(round(float_val, 0))


def to_money_str(v):
    if isinstance(v, basestring):
        v = to_float(v)
    return format(v, ',.2f')