#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/30
# @Author: Neil Steven

import base64

__all__ = [
    "base64_encode", "base64_decode"
]

ENCODING_UTF_8 = "UTF-8"


def base64_encode(text: str, encoding=ENCODING_UTF_8):
    encoded_text = base64.b64encode(text.encode(encoding))
    return str(encoded_text, encoding)


def base64_decode(text: str, encoding=ENCODING_UTF_8):
    decoded_text = base64.b64decode(text)
    return str(decoded_text, encoding)
