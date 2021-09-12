#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/7/14
# @Author: Neil Steven

import sys
import traceback
from typing import Callable

from ns_console import call_sys_pause

__all__ = [
    "boot",
    "welcome"
]


def boot(main: Callable):
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("The operation has been cancelled by user!")
    except BaseException as e:
        exc_info = (type(e), e, e.__traceback__)
        traceback.print_exception(*exc_info)
        print("Exception has occurred, press any key to exit the program.")
    finally:
        call_sys_pause()


def welcome(app_name):
    print("\n**************************************************")
    print(f"Welcome to {app_name}!\n")
    print("If you have any question or suggestion, ")
    print("please contact the author Neil Steven.")
    print("**************************************************\n")
