#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/29
# @Author: Neil Steven

import mimetypes
import shutil

from ns_path import AnyPathLike, to_path

__all__ = [
    "copy", "move", "delete",
    "get_content_type"
]


def copy(src: AnyPathLike, dst: AnyPathLike):
    src = to_path(src)
    dst = to_path(dst)
    if not src.exists():
        raise IOError(f"Could not copy the file {src} because it does not exist!")
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst) if src.is_dir() else shutil.copy(src, dst)


def move(src: AnyPathLike, dst: AnyPathLike):
    src = to_path(src)
    dst = to_path(dst)
    if not src.exists():
        raise IOError(f"Could not move the file {src} because it does not exist!")
    dst.mkdir(parents=True, exist_ok=True)
    shutil.move(src, dst)


def delete(path: AnyPathLike):
    path = to_path(path)
    if not path.exists():
        raise IOError(f"Could not delete the file {path} because it does not exist!")
    shutil.rmtree(path) if path.is_dir() else path.unlink()


def get_content_type(path: AnyPathLike) -> str:
    return mimetypes.guess_type(path)[0]
