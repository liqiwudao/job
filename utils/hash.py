# -*- coding:utf-8 -*-
import hashlib


def md5_hex(data):
    """
    shortcut of hashlib.md5('xxx').hexdigest()

    >>> md5_hex('123')
    '202cb962ac59075b964b07152d234b70'
    """
    return hashlib.md5(data).hexdigest()


def md5_stream(stream, block_size=8192):
    """Compute md5 checksum from stream"""
    md5 = hashlib.md5()
    stream.seek(0)
    while True:
        buf = stream.read(block_size)
        if not buf:
            break
        md5.update(buf)
        if len(buf) < block_size:
            break
    stream.seek(0)
    return md5.hexdigest()
