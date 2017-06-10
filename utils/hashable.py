import collections


def hashable(obj):
    if isinstance(obj, collections.Hashable):
        return obj
    if isinstance(obj, collections.Mapping):
        items = [(k, hashable(v)) for (k, v) in obj.iteritems()]
        return frozenset(items)
    if isinstance(obj, collections.Iterable):
        return tuple([hashable(item) for item in obj])
    raise TypeError(type(obj))


try:
    text = (str, unicode)
except NameError:
    text = str


def hashable_identity(obj):
    if hasattr(obj, '__func__'):
        return id(obj.__func__), id(obj.__self__)
    elif hasattr(obj, 'im_func'):
        return id(obj.im_func), id(obj.im_self)
    elif isinstance(obj, text):
        return obj
    else:
        return id(obj)
