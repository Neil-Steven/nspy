#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/30
# @Author: Neil Steven

import getpass
import os
import sys
from typing import Optional, List, Any

from ns_common import is_empty
from ns_constant import REGEX_INTEGER_NUMBER
from ns_regex import is_match

__all__ = [
    "call_sys_pause",
    "call_user_input", "call_user_input_password",
    "call_user_choose_number", "call_user_choose_from_list",
    "call_user_confirm"
]


def call_sys_pause():
    os.system("pause")


def call_user_input(prompt: Optional[str] = None, *,
                    default_value: Optional[str] = None,
                    pattern: Optional[str] = None) -> str:
    def check_valid(user_input):
        if is_empty(user_input):
            if default_value is None:
                return None
            user_input = default_value
        if pattern is None or is_match(pattern, user_input, full_match=True, ignore_case=True):
            return user_input
        return None

    prompt = "" if is_empty(prompt) else prompt + " "
    while (result := check_valid(input(prompt))) is None:
        print("Invalid input, please try again.")
    return result


def call_user_input_password(prompt: Optional[str] = None, *, allow_empty: bool = False) -> str:
    def check_valid(user_input):
        if not is_empty(user_input) or allow_empty:
            return user_input
        return None

    while (result := check_valid(getpass.getpass(prompt))) is None:
        print("Invalid input, please try again.")
    return result


def call_user_choose_number(prompt: Optional[str] = None, *,
                            default_value: Optional[int] = None,
                            from_num: Optional[int] = 0,
                            to_num: Optional[int] = sys.maxsize) -> int:
    def check_valid(user_input):
        choice = int(user_input)
        if choice in range(from_num, to_num + 1):
            return choice
        return None

    while (result := check_valid(call_user_input(prompt, default_value=str(default_value),
                                                 pattern=REGEX_INTEGER_NUMBER))) is None:
        print("Invalid input, please try again.")
    return result


def call_user_choose_from_list(the_list: List[Any], *,
                               default_value: Optional[int] = None,
                               choice_prompt: Optional[str] = None) -> Any:
    for index in range(len(the_list)):
        print(f"{index + 1}: {the_list[index]}")
    if choice_prompt is None:
        choice_prompt = "Please input your choice:"
    choose_num = call_user_choose_number(choice_prompt, default_value=default_value, from_num=1, to_num=len(the_list))
    return the_list[choose_num - 1]


def call_user_confirm(prompt: Optional[str] = None, *, default_value: Optional[bool] = None) -> bool:
    prompt_with_option = "" if is_empty(prompt) else prompt + " (y/n)"
    if default_value is None:
        user_input = call_user_input(prompt_with_option, pattern=r"(y|n|yes|no)").lower()
    else:
        default_value_string = "y" if default_value is True else "n"
        user_input = call_user_input(prompt_with_option, default_value=default_value_string,
                                     pattern=r"(y|n|yes|no)").lower()

    return True if user_input == "y" or user_input == "yes" else False
