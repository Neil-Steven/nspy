#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/30
# @Author: Neil Steven

try:
    import inflect
except ImportError:
    inflect = None
    inflect_engine = None
else:
    inflect_engine = inflect.engine()

__all__ = [
    "plural"
]


def plural(count: int, word: str) -> str:
    plural_word = word
    if count != 1:
        if inflect_engine is not None:
            plural_word = inflect_engine.plural(word)
        else:
            # If there is no inflect engine in the current environment,
            # then use the simple but not accurate rule, which works fine in the most circumstances
            if word.endswith("y"):
                plural_word = word[:-1] + "ies"
            elif word[-1] in "sx" or word[-2:] in ["sh", "ch"]:
                plural_word = word + "es"
            elif word.endswith("an"):
                plural_word = word[:-2] + "en"
            else:
                plural_word = word + "s"
    return f"{count} {plural_word}"
