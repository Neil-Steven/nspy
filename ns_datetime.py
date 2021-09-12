#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/29
# @Author: Neil Steven

from datetime import datetime

__all__ = [
    "DEFAULT_DATE_FORMAT",
    "date_to_timestamp",
    "timestamp_to_date",
    "get_current_time",
    "get_current_timestamp"
]

DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def date_to_timestamp(date: str, date_format: str = DEFAULT_DATE_FORMAT) -> int:
    formatted_datetime = datetime.strptime(date, date_format)
    return int(round(formatted_datetime.timestamp() * 1000))


def timestamp_to_date(timestamp: int, date_format: str = DEFAULT_DATE_FORMAT) -> str:
    formatted_timestamp = float(timestamp) / 1000
    return datetime.fromtimestamp(formatted_timestamp).strftime(date_format)


def get_current_time(date_format: str = DEFAULT_DATE_FORMAT) -> str:
    return datetime.now().strftime(date_format)


def get_current_timestamp() -> int:
    return int(round(datetime.now().timestamp() * 1000))
