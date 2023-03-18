#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/30
# @Author: Neil Steven

import os
from pathlib import Path
from typing import List, Union, Optional

from ns_common import is_empty

__all__ = [
    "AnyPathLike", "MultiPathLike",
    "join_path",
    "list_dir",
    "get_suffix",
    "is_file_like", "is_dir_like",
    "to_path", "to_multi_path"
]

AnyPathLike = Union[str, os.PathLike]
MultiPathLike = Union[AnyPathLike, List[AnyPathLike]]


def join_path(base_path: str, *sub_path: str) -> str:
    final_sub_path_list = []
    for cur_sub_path in sub_path:
        final_sub_path_list.append(cur_sub_path.removeprefix("/"))
    return os.path.join(base_path, *final_sub_path_list)


def list_dir(path: AnyPathLike, pattern: Optional[str] = None, *,
             absolute_path: bool = False, sort: bool = False) -> List[str]:
    path = to_path(path)
    if pattern is None:
        pattern = "*"

    result = []
    for p in path.glob(pattern):
        result.append(str(p.resolve()) if absolute_path else p.name)
    return result if not sort else sorted(result)


def get_suffix(path: AnyPathLike, *, full: bool = True, with_point: bool = True) -> str:
    path = to_path(path)
    suffix = path.suffix if not full else "".join(path.suffixes)
    if not with_point and suffix.startswith("."):
        suffix = suffix[1:]
    return suffix


def is_file_like(path: AnyPathLike) -> bool:
    path = to_path(path)
    if path.exists():
        return path.is_file()
    return not is_empty(path.suffix)


def is_dir_like(path: AnyPathLike) -> bool:
    path = to_path(path)
    if path.exists():
        return path.is_dir()
    return is_empty(path.suffix)


def to_path(path: AnyPathLike) -> Path:
    return path if isinstance(path, Path) else Path(path)


def to_multi_path(path: MultiPathLike) -> List[Path]:
    return [to_path(p) for p in path] if isinstance(path, list) else [to_path(path)]
