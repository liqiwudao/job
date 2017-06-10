# -*- coding:utf-8 -*-
from random import choice
import string
import time

_chars = string.printable[:87] + '_' + string.printable[90:95]


def random_str(length=6, chars=_chars):
    return ''.join(choice(chars) for i in range(length))


def random_ticket():
    """
    Randomize ticket with current timestamp
    :return:
    """
    ts = time.time()
    return "%s_%s" % (ts, random_str(6, string.digits))