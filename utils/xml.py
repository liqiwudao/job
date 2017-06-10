# -*- coding:utf-8 -*-
from collections import defaultdict
from lxml import etree


def etree_to_dict(t):
    """Convert etree to dict object

    This gist is from
    http://stackoverflow.com/questions/7684333/converting-xml-to-dictionary-using-elementtree

    :param t:
    :return: dict
    :rtype dict
    """
    tag = t.tag
    d = {tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.iteritems():
                dd[k].append(v)
        d = {tag: {k: v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[tag]['#text'] = text
        else:
            d[tag] = text
    return d


def parse_xml_string(text, **options):
    """
    Parse simple xml response into dict object

    :param text:
    :type text:str
    :return:
    :rtype:dict
    """
    parser = etree.XMLParser(remove_blank_text=True, **options)
    root = etree.fromstring(text, parser)
    return etree_to_dict(root)
