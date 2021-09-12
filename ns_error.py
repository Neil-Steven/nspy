#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/30
# @Author: Neil Steven

__all__ = [
    "CustomRuntimeError"
]


class CustomRuntimeError(RuntimeError):
    def __init__(self, message, return_code):
        self.message = message
        self.return_code = return_code

    def __str__(self):
        return self.message
