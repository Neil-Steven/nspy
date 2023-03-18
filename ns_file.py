#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/29
# @Author: Neil Steven

import hashlib
import mimetypes
import shutil
from typing import IO

from ns_path import AnyPathLike, to_path
from ns_string import fuzzy_format

__all__ = [
    "copy", "move", "delete",
    "get_content_type",
    "smart_open",
    "hash_file"
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


def smart_open(file, **kwargs) -> IO:
    from chardet import UniversalDetector
    with open(file, 'rb') as detect_handler:
        detector = UniversalDetector()
        for line in detect_handler.readlines():
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    kwargs["encoding"] = detector.result["encoding"]
    return open(file, **kwargs)


def hash_file(file_path: str, algorithm: str, chuck_size: int = 8192) -> str:
    algorithm = fuzzy_format(algorithm)
    match algorithm:
        case "md5":
            hash_method = hashlib.md5
        case "sha1":
            hash_method = hashlib.sha1
        case "sha224":
            hash_method = hashlib.sha224
        case "sha256":
            hash_method = hashlib.sha256
        case "sha384":
            hash_method = hashlib.sha384
        case "sha512":
            hash_method = hashlib.sha512
        case _:
            raise ValueError(f"Hash algorithm '{algorithm}' is unsupported!")

    with open(file_path, 'rb') as f:
        hash_obj = hash_method()
        while chunk := f.read(chuck_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()
