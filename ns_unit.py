#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/7/8
# @Author: Neil Steven

from typing import Optional

from ns_regex import is_match, search

__all__ = [
    "humanize_file_size", "parse_humanized_file_size"
]

KB_UNITS = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB", "BB", "NB", "DB", "CB", "XB"]
KiB_UNITS = ["B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB", "BiB", "NiB", "DiB", "CiB", "XiB"]


def humanize_file_size(byte_size: int, target_unit: Optional[str] = None, *,
                       digit: Optional[int] = 3, add_blank: bool = True) -> str:
    """
    Convert the size number (bytes) which is not quite readable to a much more readable one.
    If the target unit is None, then it will choose an appropriate unit automatically.
    """
    if target_unit is None or target_unit.upper() in KB_UNITS:
        unit_list = KB_UNITS
        radix = 1000
    elif target_unit.upper() in [u.upper() for u in KiB_UNITS]:
        unit_list = KiB_UNITS
        radix = 1024
    else:
        raise ValueError(f"Target unit '{target_unit}' is invalid!")

    result = float(byte_size)
    unit = target_unit

    target_round = unit_list.index(unit) if unit is not None else 9999
    cur_round = 0
    while cur_round < target_round:
        if unit is None and result < radix:
            unit = unit_list[cur_round]
            break
        cur_round += 1
        result /= radix

    blank = " " if add_blank else ""
    return f"{round(result, digit)}{blank}{unit}"


def parse_humanized_file_size(readable_size: str) -> int:
    """
    Parse a readable size string to a normal number (bytes).
    """
    readable_size = readable_size.strip()
    if not is_match(r"\d+(\.\d+)?\s*[A-Za-z]{1,3}", readable_size, full_match=True, ignore_case=True):
        raise ValueError(f"'{readable_size}' is not a parsable readable size!")

    result = float(search(r"\d+(\.\d+)?", readable_size))
    unit = search(r"[A-Za-z]{1,3}", readable_size)

    unit_length = len(unit)
    if 1 <= unit_length <= 2:
        unit_list = KB_UNITS
        radix = 1000
    elif unit_length == 3:
        unit_list = KiB_UNITS
        radix = 1024
    else:
        raise ValueError(f"'{unit}' is not a valid unit!")

    target_round = [u.upper() for u in unit_list].index(unit.upper())
    cur_round = 0
    while cur_round < target_round:
        cur_round += 1
        result *= radix

    return int(result)
