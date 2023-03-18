#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2023/02/03
# @Author: Neil Steven

from typing import Any

from ns_string import fuzzy_match

__all__ = [
    "fuzzy_dict_get"
]


def fuzzy_dict_get(dictionary: dict[str, Any], name: str, pop: bool = False, fallback: Any = None) -> Any | None:
    for cur_key in dictionary.keys():
        if fuzzy_match(cur_key, name):
            return dictionary.pop(cur_key) if pop else dictionary[cur_key]
    return fallback
