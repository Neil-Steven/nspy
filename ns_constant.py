#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/7/15
# @Author: Neil Steven

REGEX_INTEGER_NUMBER = r"(\+|-)?(\d+)"
REGEX_FLOAT_NUMBER = r"(\+|-)?(\d+)(\.\d+)?"

REGEX_CHINESE_CHAR = r"[\u4e00-\u9fa5]{0,}"
REGEX_CHINESE_PHONE_NUMBER = r"(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}"
REGEX_DOMAIN = r"[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(/.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+/.?"
REGEX_EMAIL = r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
REGEX_IDENTIFY_CARD = r"[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]"
REGEX_IPV4 = r"((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}"
