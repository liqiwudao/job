# -*- coding:utf-8 -*-
__author__ = 'night'

from collections import defaultdict, namedtuple
import re


class DotDict(dict):
    """ A dictionary with attribute-style access. Maps attribute
        access to dictionary.

        >>> d = DotDict(a=1, b=2)
        >>> sorted(d.items())
        [('a', 1), ('b', 2)]
        >>> d.a
        1

        >>> d.c = 3
        >>> d.c
        3
        >>> d.d # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        AttributeError: ...
    """
    __slots__ = ()

    def __setattr__(self, key, value):
        return super(DotDict, self).__setitem__(key, value)

    def __getattr__(self, name):
        try:
            return super(DotDict, self).__getitem__(name)
        except KeyError:
            raise AttributeError(name)


class DefaultDotDict(defaultdict):
    """ A dictionary with attribute-style access. Maps attribute
        access to dictionary.

        >>> d = DefaultDotDict(str, a=1, b=2)
        >>> d.a
        1

        >>> d.c = 3
        >>> d.c
        3
        >>> d.d
        ''
    """
    __slots__ = ()

    def __setattr__(self, key, value):
        return super(DefaultDotDict, self).__setitem__(key, value)

    def __getattr__(self, name):
        return super(DefaultDotDict, self).__getitem__(name)


class CamelCaseDict(dict):
    """
    A dictionary will convert all CamelCase key to camel_case and store

    >>> d = CamelCaseDict()
    >>> d['TestCase'] = 1
    >>> d.test_case
    1
    >>> d['test_case']
    1
    >>> d.TestCase
    1
    >>> d['TestCase']
    1
    """
    __slots__ = ()
    first_cap_re = re.compile('(.)([A-Z][a-z]+)')
    all_cap_re = re.compile('([a-z0-9])([A-Z])')

    def convert(self, name):
        s1 = self.first_cap_re.sub(r'\1_\2', name)
        return self.all_cap_re.sub(r'\1_\2', s1).lower()

    def __setattr__(self, key, value):
        return self.__setitem__(key, value)

    def __setitem__(self, key, value):
        return super(CamelCaseDict, self).__setitem__(self.convert(key), value)

    def __getitem__(self, item):
        return super(CamelCaseDict, self).__getitem__(self.convert(item))

    def __getattr__(self, name):
        try:
            return self.__getitem__(name)
        except KeyError:
            raise AttributeError(name)


# stolen from mongokit
class EvalException(Exception):
    pass


class DotExpandedDict(dict):
    """
    A special dictionary constructor that takes a dictionary in which the keys
    may contain dots to specify inner dictionaries. It's confusing, but this
    example should make sense.

    >>> d = DotExpandedDict({'person.1.firstname': ['Simon'], \
          'person.1.lastname': ['Willison'], \
          'person.2.firstname': ['Adrian'], \
          'person.2.lastname': ['Holovaty']})
    >>> d
    {'person': {'1': {'lastname': ['Willison'], 'firstname': ['Simon']},
    '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}}
    >>> d['person']
    {'1': {'lastname': ['Willison'], 'firstname': ['Simon']}, '2': {'lastname': ['Holovaty'], 'firstname': ['Adrian']}}
    >>> d['person']['1']
    {'lastname': ['Willison'], 'firstname': ['Simon']}

    # Gotcha: Results are unpredictable if the dots are "uneven":
    >>> DotExpandedDict({'c.1': 2, 'c.2': 3, 'c': 1})
    {'c': 1}
    """
    # code taken from Django source code http://code.djangoproject.com/
    def __init__(self, key_to_list_mapping):
        for k, v in key_to_list_mapping.items():
            current = self
            bits = k.split('.')
            for bit in bits[:-1]:
                if bit.startswith('$'):
                    try:
                        bit = eval(bit[1:])
                    except:
                        raise EvalException('%s is not a python type' % bit[:1])
                current = current.setdefault(bit, {})
            # Now assign value to current position
            last_bit = bits[-1]
            if last_bit.startswith('$'):
                try:
                    last_bit = eval(last_bit[1:])
                except:
                    raise EvalException('%s is not a python type' % last_bit)
            try:
                current[last_bit] = v
            except TypeError:  # Special-case if current isn't a dict.
                current = {last_bit: v}


class DotCollapsedDict(dict):
    """
    A special dictionary constructor that take a dict and provides
    a dot collapsed dict:

    >>> DotCollapsedDict({'a':{'b':{'c':{'d':3}, 'e':5}, "g":2}, 'f':6})
    {'a.b.c.d': 3, 'a.b.e': 5, 'a.g': 2, 'f': 6}

    >>> DotCollapsedDict({'bla':{'foo':{unicode:{"bla":3}}, 'bar':'egg'}})
    {'bla.foo.$unicode.bla': 3, 'bla.bar': "egg"}

    >>> DotCollapsedDict({'bla':{'foo':{unicode:{"bla":3}}, 'bar':'egg'}}, remove_under_type=True)
    {'bla.foo':{}, 'bla.bar':unicode}

    >>> dic = {'bar':{'foo':3}, 'bla':{'g':2, 'h':3}}
    >>> DotCollapsedDict(dic, reference={'bar.foo':None, 'bla':{'g':None, 'h':None}})
    {'bar.foo':3, 'bla':{'g':2, 'h':3}}

    """

    def __init__(self, passed_dict, remove_under_type=False, reference=None):
        self._remove_under_type = remove_under_type
        assert isinstance(passed_dict, dict), "you must pass a dict instance"
        final_dict = {}
        self._reference = reference
        self._make_dotation(passed_dict, final_dict)
        self.update(final_dict)

    def _make_dotation(self, d, final_dict, key=""):
        for k, v in d.iteritems():
            if isinstance(k, type):
                k = "$%s" % k.__name__
            if isinstance(v, dict) and v != {}:
                if key:
                    _key = "%s.%s" % (key, k)
                else:
                    _key = k
                if self._reference and _key in self._reference:
                    final_dict[_key] = v
                if self._remove_under_type:
                    if [1 for i in v.keys() if isinstance(i, type)]:
                        v = v.__class__()
                        if not key:
                            final_dict[k] = v
                        else:
                            final_dict["%s.%s" % (key, k)] = v
                    else:
                        self._make_dotation(v, final_dict, _key)
                else:
                    self._make_dotation(v, final_dict, _key)
            else:
                if not key:
                    final_dict[k] = v
                else:
                    if not self._reference:
                        final_dict["%s.%s" % (key, k)] = v
                    elif "%s.%s" % (key, k) in self._reference:
                        final_dict["%s.%s" % (key, k)] = v
                        # else:
                        #    final_dict[key] = {k: v}
                        #    print "+++", {k:v}


# FieldConstant = namedtuple('FieldConstant', ['int_val', 'str_val', 'title'])

class FieldConstant(namedtuple('FieldConstant', ['int_val', 'str_val', 'title'])):
    def __eq__(self, other):
        if isinstance(other, FieldConstant):
            return self is other
        elif isinstance(other, basestring):
            return self.str_val == other
        return self.int_val == other


_enum_types = dict()


class FieldConstantEnumType(object):
    __slots = ()

    def __init__(self, enum_type):
        self.enum_type = enum_type

    def __contains__(self, item):
        for enum in _enum_types.get(self.enum_type, ()):
            if enum.int_val == item:
                return True
        return False

    def __getattr__(self, name):
        enum_vars = _enum_types.get(self.enum_type)
        for f in enum_vars:
            if f.str_val == name:
                setattr(self, name, f)
                return f
        raise AttributeError('{0} is not valid enum value'.format(name))

    def get(self, value):
        for enum_val in _enum_types.get(self.enum_type, ()):
            if value in (enum_val.int_val, enum_val.str_val):
                return enum_val
        return None


def make_constant_enums(type_name, *type_values):
    _enum_types[type_name] = tuple(FieldConstant(*v) for v in type_values)
    return FieldConstantEnumType(type_name)


def key_sort(data):
    """
    sort by dict key and return sorted list

    :param data:  dict to sort
    :type data: dict
    :return: sorted list of k,v tuple
    :rtype: list
    """
    return [(k, data[k]) for k in sorted(data.keys())]


def recursive_sort(data):
    """
    Recursive sort dict
    :param data: data to sort
    :type data: dict
    :return: sorted list
    :rtype: list
    """
    result = []
    for k, v in key_sort(data):
        if v is dict:
            v = key_sort(v)
        result.append((k, v))
    return result
