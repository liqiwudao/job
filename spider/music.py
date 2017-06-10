#!/usr/bin/env python
# -*- coding: utf-8
__author__ = 'zjw'

import requests
import json
from bs4 import BeautifulSoup

# time_ = raw_input('input num:')

# data = {'type':'range','start': time_, 'end': time_}
header = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'no-cache',
    'Host':'music.163.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'

        }



def test(url, filename, **kwargs):
    with open(filename, 'rb') as f:
        content = f.read()
    html = content
    soup = BeautifulSoup(html, 'html.parser')
    a_list = {}

    for i in soup.select('.txt a b'):
        song_id = i.parent.attrs.get("href")[9:]
        name = i.text
        data = {
            'name': name,
            'song_id': song_id,
        }

        ret = requests.post(url, data=data)
        if not ret.ok:
            print song_id, "False", ret.status_code

if __name__ == '__main__':
    url = 'http://127.0.0.1:8002/api/song/'
    filename = 'test.html'
    test(url, filename)
