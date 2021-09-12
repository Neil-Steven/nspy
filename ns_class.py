#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/7/16
# @Author: Neil Steven

import threading

from ns_type import Typed

__all__ = [
    "TypedClass",
    "singleton", "ExplicitSingleton"
]


class TypedClass(object):
    """
    The class that can automatically handle Typed properties.
    """

    TYPED_ATTR_PREFIX = "_typed_attr_"

    def __getattribute__(self, name):
        attr = object.__getattribute__(self, name)
        if isinstance(attr, Typed):
            try:
                attr = object.__getattribute__(self, f"{TypedClass.TYPED_ATTR_PREFIX}{name}")
            except AttributeError:
                if attr.default_value is None:
                    raise AttributeError("The typed object with no default value must be initialized before using!")
                setattr(self, name, attr.default_value)
                attr = object.__getattribute__(self, f"{TypedClass.TYPED_ATTR_PREFIX}{name}")
        return attr

    def __setattr__(self, name, value):
        if name in self.__dict__:
            attr = object.__getattribute__(self, name)
            if isinstance(attr, Typed):
                if attr.expected_type != type(value):
                    if attr.strict:
                        raise TypeError(f"The value {value} is not the expected type {attr.expected_type}!")
                    value = attr.convert(value)
                return object.__setattr__(self, f"{TypedClass.TYPED_ATTR_PREFIX}{name}", value)
        return object.__setattr__(self, name, value)


def singleton(cls):
    """
    The singleton decorator.
    """

    _instance = {}
    _lock = threading.Lock()

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            with _lock:
                _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


class ExplicitSingleton(object):
    """
    The explicit singleton super class, which can only be obtained by 'instance' function.
    """

    _lock = threading.Lock()

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            with cls._lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = cls()
        return cls._instance
