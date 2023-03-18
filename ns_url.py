#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2023/01/29
# @Author: Neil Steven

from urllib.parse import urlparse, urlunparse

from ns_path import join_path

__all__ = [
    "join_url"
]


def join_url(base: str, path: str, *sub_path: str) -> str:
    arr = urlparse(base)
    path = join_path(arr.path, path, *sub_path)
    return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))
