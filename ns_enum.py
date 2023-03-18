#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2023/01/17
# @Author: Neil Steven

from enum import Enum
from typing import TypeVar

from ns_string import fuzzy_match

ENUM = TypeVar("ENUM", Enum, Enum)

__all__ = [
    "fuzzy_enum_get"
]


def fuzzy_enum_get(enum_class: type(ENUM), name: str) -> ENUM | None:
    for cur_enum in enum_class:
        if isinstance(cur_enum.value, str) and fuzzy_match(cur_enum.value, name):
            return cur_enum
        if isinstance(cur_enum.value, (list, set, tuple)):
            for v in cur_enum.value:
                if fuzzy_match(v, name):
                    return cur_enum
        if fuzzy_match(cur_enum.name, name):
            return cur_enum
    return None
