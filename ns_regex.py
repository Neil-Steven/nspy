#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/29
# @Author: Neil Steven

import re

__all__ = [
    "is_match", "match",
    "contains", "search"
]


def is_match(pattern: str, text: str, *, full_match: bool = False, ignore_case: bool = False) -> bool:
    return True if match(pattern, text, full_match=full_match, ignore_case=ignore_case) is not None else False


def match(pattern: str, text: str, *, full_match: bool = False, ignore_case: bool = False) -> str:
    if full_match:
        pattern = "^(" + pattern + ")$"
    flag = re.IGNORECASE if ignore_case else 0
    result = re.match(pattern, text, flag)
    if result is not None:
        return result.group()


def contains(pattern: str, text: str, *, ignore_case: bool = True) -> bool:
    return True if search(pattern, text, ignore_case=ignore_case) is not None else False


def search(pattern: str, text: str, *, ignore_case: bool = True) -> str:
    flag = re.IGNORECASE if ignore_case else 0
    result = re.search(pattern, text, flag)
    if result is not None:
        return result.group()
