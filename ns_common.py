#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/29
# @Author: Neil Steven

__all__ = [
    "is_basic_type",
    "is_empty"
]


def is_basic_type(o):
    return isinstance(o, int) or isinstance(o, float) or isinstance(o, bool) or isinstance(o, complex)


def is_empty(o):
    if is_basic_type(o):
        return False
    if isinstance(o, str):
        return len(o.strip()) == 0
    return o is None or len(o) == 0
