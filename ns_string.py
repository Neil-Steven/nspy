#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/7/6
# @Author: Neil Steven

import sys

__all__ = [
    "is_same_version",
    "remove_prefix", "remove_suffix"
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


# Reference https://www.python.org/dev/peps/pep-0616/
def remove_prefix(self: str, prefix: str, /) -> str:
    if sys.version_info >= (3, 9):
        return self.removeprefix(prefix)
    else:
        return self[len(prefix):] if self.startswith(prefix) else self[:]


# Reference https://www.python.org/dev/peps/pep-0616/
def remove_suffix(self: str, suffix: str, /) -> str:
    if sys.version_info >= (3, 9):
        return self.removesuffix(suffix)
    else:
        return self[:-len(suffix)] if suffix and self.endswith(suffix) else self[:]
