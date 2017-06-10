#-*- coding:utf-8 -*-
import inspect
from werkzeug.utils import import_string, find_modules

# from ..log import daisy_logger


def get_imported_stuff_by_path(path):
    module_name, object_name = path.rsplit('.', 1)
    module = import_string(module_name)
    return module, object_name


def find_module_classes(path, cls=None):
    for modname in find_modules(path, False, True):
        module = import_string(modname, True)
        if module:
            predicate = lambda c: inspect.isclass(c) and c.__module__ == modname and issubclass(c, cls)
            for name, obj in inspect.getmembers(module, predicate):
                # daisy_logger.debug("found class(subclass of %s): %s => %s" % (cls, name, obj))
                yield obj


def get_module_exported_dict(module):
    if inspect.ismodule(module):
        results = {}
        for name in filter(lambda x: not x.startswith('_'), dir(module)):
            results[name] = getattr(module, name)
        return results
    return