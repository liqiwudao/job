#!/usr/bin/env python
# encoding: utf-8
"""
string.py

string utility


"""

import re
import datetime


# douban-utils copy begin.
# follow code block were copy from douban-utils (https://github.com/douban/douban-utils)

def trunc_utf8(string, num, etc="..."):
    """truncate a utf-8 string, show as num chars.
    arg: string, a utf-8 encoding string; num, look like num chars
    return: a utf-8 string
    """
    gb = string.decode("utf8", "ignore").encode("gb18030", "ignore")
    if num >= len(gb):
        return string
    ret = gb[:num].decode("gb18030", "ignore").encode("utf8")
    if etc:
        ret += etc
    return ret


def decode_utf8_str(c):
    try:
        if isinstance(c, unicode):
            return c
        content = unicode(c, 'utf8', errors='replace')
    except TypeError:
        content = unicode(c, errors='replace')
    return content


def trunc_short(s, max_len=210, etc="..."):
    s = decode_utf8_str(s)
    if len(s) >= max_len:
        s = s[:max_len] + unicode(etc)
    return s


def utf8_length(string):
    return string and len(string.decode("utf8", "ignore").encode("gb18030", "ignore")) or 0


def trunc_utf8_by_char(s, num, etc="..."):
    unistr = decode_utf8_str(s)
    if num >= len(unistr):
        return s
    s2 = unistr[:num].encode("utf8")
    if etc:
        s2 += etc
    return s2


def js_quote(js):
    return js.replace('\\', r'\\').replace('\r', r'\r') \
        .replace('\n', r'\n').replace("'", r"\'").replace('"', r'\"')


EMAILRE = re.compile(r'^[_\.0-9a-zA-Z+-]+@([0-9a-zA-Z]+[0-9a-zA-Z-]*\.)+[a-zA-Z]{2,4}$')


def is_valid_email(email):
    if len(email) >= 6:
        return EMAILRE.match(email) != None
    return False


def format_rfc822_date(dt, localtime=True, cookie_format=False):
    if localtime:
        dt = dt - datetime.timedelta(hours=8)
    fmt = "%s, %02d %s %04d %02d:%02d:%02d GMT"
    if cookie_format:
        fmt = "%s, %02d-%s-%04d %02d:%02d:%02d GMT"

    # dt.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
    return fmt % (
        ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()],
        dt.day,
        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][dt.month - 1],
        dt.year, dt.hour, dt.minute, dt.second)


def format_cookie_date(dt, localtime=True):
    return format_rfc822_date(dt, localtime=True, cookie_format=True)


def is_ascii_string(text):
    if not isinstance(text, basestring):
        return False
    replace = [c for c in text if not (' ' <= c <= '~')]
    if replace:
        return False
    else:
        return True


# douban-utils end.


def str2bool(s, default=False):
    """Convert str to bool value

    >>> str2bool('') or str2bool(u'') or str2bool(None)
    False
    >>> str2bool('on') and str2bool(u'on') and str2bool(u'1') and str2bool('1')
    True
    """
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


_first_cap_re = re.compile('(.)([A-Z][a-z]+)')
_all_cap_re = re.compile('([a-z0-9])([A-Z])')


def dashify(name):
    s1 = _first_cap_re.sub(r'\1-\2', name)
    return _all_cap_re.sub(r'\1-\2', s1).lower()


def camel_to_snake(name):
    s1 = _first_cap_re.sub(r'\1_\2', name)
    snake_str = _all_cap_re.sub(r'\1_\2', s1).lower()
    return snake_str.replace('__', '_')


def dash_to_camel(dashed_str):
    return _convert_to_camel(dashed_str, '-')


def snake_to_camel(snake_str):
    return _convert_to_camel(snake_str, '_')


def snake_to_cap(snake_str):
    return _convert_to_camel(snake_str, '_', True)


def _convert_to_camel(snake_cased_str, separator, first_cap=False):
    components = snake_cased_str.split(separator)
    preffix = ""
    suffix = ""
    if components[0] == "":
        components = components[1:]
        preffix = separator
    if components[-1] == "":
        components = components[:-1]
        suffix = separator
    if len(components) > 1:
        camel_cased_str = components[0].title() if first_cap else components[0].lower()
        for x in components[1:]:
            if x.isupper() or x.istitle():
                camel_cased_str += x
            else:
                camel_cased_str += x.title()
    else:
        camel_cased_str = components[0].title()
    return preffix + camel_cased_str + suffix


def quote_xml(in_str):
    if not in_str:
        return ''
    s1 = (isinstance(in_str, basestring) and in_str or
          '%s' % in_str)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_xml_attrib(in_str):
    s1 = (isinstance(in_str, basestring) and in_str or
          '%s' % in_str)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1
