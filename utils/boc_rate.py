# -*- coding:utf-8 -*-
__author__ = 'night'
import requests
from cssselect import parser
from lxml.html import fromstring
from . import convert, datetimeutil


def _parse_prc_time(ts):
    return datetimeutil.parse_utc_from_str(ts, 'Asia/Shanghai', '%Y-%m-%d%H:%M:%S')


def fetch_boc_exchange_rate():
    """
    获取中国银行实时外汇牌价,目前只获取第一页的货币汇率

    Return dict like:
    {
        currency_code: {'buy', 'cash_buy', 'selling', 'cash_selling', 'middle', 'pub_time'}
    }

    :return:
    """
    try:
        html = requests.session().get('http://www.boc.cn/sourcedb/whpj/enindex.html', timeout=60).text
    except requests.ConnectionError:
        return
    doc = fromstring(html)
    trs = doc.cssselect('table tr[align=center]')
    result = {}
    for tr in trs:
        tds = list(tr)
        currency_code = tds[0].text.strip().upper()
        record = {
            'buy': round(convert.to_float(tds[1].text) / 100, 4),
            'cash_buy': round(convert.to_float(tds[2].text) / 100, 4),
            'selling': round(convert.to_float(tds[3].text) / 100, 4),
            'cash_selling': round(convert.to_float(tds[4].text) / 100, 4),
            'middle': round(convert.to_float(tds[5].text) / 100, 4),
            'pub_time': _parse_prc_time(tds[6].text.replace(u"\xa0\n\t\t", ''))
        }
        result[currency_code] = record
    return result
