#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/7/6
# @Author: Neil Steven

import re

__all__ = [
    "is_same_version",
    "fuzzy_format",
    "fuzzy_match"
]


def is_same_version(v1: str, v2: str) -> bool:
    v1_split = [each.strip() for each in v1.split(".")]
    v2_split = [each.strip() for each in v2.split(".")]
    longer_ver = v1_split if len(v1_split) > len(v2_split) else v2_split
    shorter_ver = v2_split if v1_split == longer_ver else v1_split

    for index in range(len(longer_ver)):
        if index < len(shorter_ver):
            cur_v1_ver_num = v1_split[index]
            cur_v2_ver_num = v2_split[index]
            if cur_v1_ver_num != cur_v2_ver_num:
                return False
        else:
            cur_longer_ver_num = longer_ver[index]
            if cur_longer_ver_num != "0":
                return False
    return True


def fuzzy_format(string: str, ignore_char_pattern: str = r"[\s\-_]", substitute: str = "") -> str:
    return re.sub(ignore_char_pattern, substitute, string.lower())


def fuzzy_match(string: str, other: str) -> bool:
    return fuzzy_format(string) == fuzzy_format(other)
