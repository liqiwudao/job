# -*- coding:utf-8 -*-
"""
Receipt for Base64 convert
code from this:

http://stackoverflow.com/questions/1119722/base-62-conversion-in-python?lq=1

"""

import string


# integer n-base convert
BASE_LIST = string.digits + string.letters
BASE_DICT = dict((c, i) for i, c in enumerate(BASE_LIST))


def base_decode(string, reverse_base=BASE_DICT):
    """
    Decode x-based string to 10-based integer

    >>> base_decode('g8')
    1000

    >>> base_decode('babb', ['1','2','3','a','b','c'])
    1000

    :param string:
    :type string:
    :param reverse_base:
    :type reverse_base:
    :return:
    :rtype:
    """
    length = len(reverse_base)
    ret = 0
    for i, c in enumerate(string[::-1]):
        ret += (length ** i) * reverse_base[c]

    return ret


def base_encode(integer, base=BASE_LIST):
    """
    Encode integer to the x-based string

    >>> base_encode(1000)
    'g8'

    >>> base_encode(1000, ['1','2','3','a','b','c'])
    'babb'

    :param integer:
    :type integer:
    :param base:
    :type base:
    :return:
    :rtype: str
    """
    length = len(base)
    ret = ''
    while integer != 0:
        ret = base[integer % length] + ret
        integer /= length

    return ret
