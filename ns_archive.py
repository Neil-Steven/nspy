#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/29
# @Author: Neil Steven

import bz2
import gzip
import lzma
import tarfile
import zipfile
from pathlib import Path
from typing import List, Tuple, Optional

from ns_common import is_empty
from ns_file import delete
from ns_path import AnyPathLike, MultiPathLike, get_suffix, to_path, to_multi_path
from ns_regex import is_match

try:
    import py7zr
except ImportError:
    py7zr = None

try:
    import rarfile
except ImportError:
    rarfile = None

__all__ = [
    "compress", "make_zip", "make_7z", "make_tar", "make_gz", "make_bz2", "make_xz",
    "decompress", "un_zip", "un_rar", "un_7z", "un_tar", "un_gz", "un_bz2", "un_xz"
]


def compress(src: MultiPathLike, dst: AnyPathLike, *, delete_src: bool = False) -> str:
    """
    The convenience way to compress files.

    Attention:
    1. Compress file with password is unsupported
    2. rar compression is unsupported
    3. gz/bz2/xz only support compressing single file
    """
    suffixes = get_suffix(dst, full=True)
    if suffixes.endswith(".zip"):
        return make_zip(src, dst, delete_src=delete_src)
    elif suffixes.endswith(".7z"):
        return make_7z(src, dst, delete_src=delete_src)
    elif is_match(r".*\.(tar\.(gz|xz|bz)|(t(gz|xz|bz|bz2|b2)))$", suffixes):
        return make_tar(src, dst, delete_src=delete_src)
    elif is_match(r".*\.(gz|bz2|xz)$", suffixes):
        if isinstance(src, list):
            if len(src) > 1:
                raise ValueError("Compress more than one file to a gz/bz2/xz file is not supported!")
            src = src[0]

        if suffixes.endswith(".gz"):
            return make_gz(src, dst, delete_src=delete_src)
        elif suffixes.endswith(".bz2"):
            return make_bz2(src, dst, delete_src=delete_src)
        else:
            return make_xz(src, dst, delete_src=delete_src)
    else:
        raise ValueError(f"File type '{suffixes}' is not supported for compressing!")


def make_zip(src: MultiPathLike, dst: AnyPathLike, *, store_only: bool = False, delete_src: bool = False) -> str:
    src_path_list, dst_path = _compress_check(src, dst)
    zip_mode = zipfile.ZIP_STORED if store_only else zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(dst, "w", zip_mode) as zip_file:
        for each in src_path_list:
            zip_file.write(each)

        if delete_src:
            for each in src_path_list:
                delete(each)
        return str(dst_path.resolve())


def make_7z(src: MultiPathLike, dst: AnyPathLike, *, delete_src: bool = False) -> str:
    # Attention: the python lib 'py7zr' is needed.
    if py7zr is None:
        raise RuntimeError("The lib 'py7zr' is needed for the make_7z operation!")

    src_path_list, dst_path = _compress_check(src, dst)
    with py7zr.SevenZipFile(dst, "w") as seven_zip_file:
        for each in src_path_list:
            seven_zip_file.write(each)

        if delete_src:
            for each in src_path_list:
                delete(each)
        return str(dst_path.resolve())


def make_tar(src: MultiPathLike, dst: AnyPathLike, compression: Optional[str] = None, *,
             delete_src: bool = False) -> str:
    src_path_list, dst_path = _compress_check(src, dst)
    with tarfile.open(dst, _get_tar_mode(dst_path, "w", compression)) as tar_file:
        for each in src_path_list:
            tar_file.add(each)

        if delete_src:
            for each in src_path_list:
                delete(each)
        return str(dst_path.resolve())


def make_gz(src: AnyPathLike, dst: AnyPathLike, *, delete_src: bool = False) -> str:
    src_path_list, dst_path = _compress_check(src, dst)
    with open(src_path_list[0], "rb") as input_file:
        with gzip.GzipFile(dst, "w") as gz_file:
            gz_file.write(input_file.read())

        if delete_src:
            delete(src)
        return str(dst_path.resolve())


def make_bz2(src: AnyPathLike, dst: AnyPathLike, *, delete_src: bool = False) -> str:
    src_path_list, dst_path = _compress_check(src, dst)
    with open(src_path_list[0], "rb") as input_file:
        with bz2.BZ2File(dst, "w") as bz_file:
            bz_file.write(input_file.read())

        if delete_src:
            delete(src)
        return str(dst_path.resolve())


def make_xz(src: AnyPathLike, dst: AnyPathLike, *, delete_src: bool = False) -> str:
    src_path_list, dst_path = _compress_check(src, dst)
    with open(src_path_list[0], "rb") as input_file:
        with lzma.LZMAFile(dst, "w") as xz_file:
            xz_file.write(input_file.read())

        if delete_src:
            delete(src)
        return str(dst_path.resolve())


def decompress(src: AnyPathLike, dst_dir: AnyPathLike, *,
               pattern: Optional[str] = None, password: Optional[str] = None, delete_src: bool = False) -> List[str]:
    """
    The convenience way to decompress a file.

    Attention:
        1. Only zip/rar/7z support being decompressed with password
        2. gz file does not support specifying pattern
    """
    suffixes = get_suffix(src, full=True)
    if suffixes.endswith(".zip"):
        return un_zip(src, dst_dir, pattern=pattern, password=password, delete_src=delete_src)
    elif suffixes.endswith(".rar"):
        return un_rar(src, dst_dir, pattern=pattern, password=password, delete_src=delete_src)
    elif suffixes.endswith(".7z"):
        return un_7z(src, dst_dir, pattern=pattern, password=password, delete_src=delete_src)
    elif is_match(r".*\.(tar\.(gz|xz|bz)|(t(gz|xz|bz|bz2|b2)))$", suffixes):
        if password is not None:
            raise ValueError("Tar file does not support being decompressed with password!")
        return un_tar(src, dst_dir, pattern=pattern, compression=None, delete_src=delete_src)
    elif is_match(r".*\.(gz|bz2|xz)$", suffixes):
        if pattern is not None:
            raise ValueError("Specify pattern to a gz/bz2/xz file is not supported!")
        if password is not None:
            raise ValueError("gz/bz2/xz file does not support being decompressed with password!")

        if suffixes.endswith(".gz"):
            return [un_gz(src, dst_dir, delete_src=delete_src)]
        elif suffixes.endswith(".bz2"):
            return [un_bz2(src, dst_dir, delete_src=delete_src)]
        else:
            return [un_xz(src, dst_dir, delete_src=delete_src)]
    else:
        raise ValueError(f"File type '{suffixes}' is not supported for decompressing!")


def un_zip(src: AnyPathLike, dst_dir: AnyPathLike, *,
           pattern: Optional[str] = None, password: Optional[str] = None, delete_src: bool = False) -> List[str]:
    src_path, dst_dir_path = _decompress_check(src, dst_dir)
    with zipfile.ZipFile(src_path, "r") as zip_file:
        if pattern is None:
            matched_inner_files = zip_file.namelist()
        else:
            matched_inner_files = [inner_file for inner_file in zip_file.namelist()
                                   if is_match(pattern, inner_file)]
            zip_file.extractall(dst_dir, matched_inner_files, password)
        if delete_src:
            delete(src_path)
        return [str(dst_dir_path.resolve() / inner_file) for inner_file in matched_inner_files]


def un_rar(src: AnyPathLike, dst_dir: AnyPathLike, *,
           pattern: Optional[str] = None, password: Optional[str] = None, delete_src: bool = False) -> List[str]:
    # Attention: the python lib 'rarfile' and UnRAR command line tool are both needed.
    if rarfile is None:
        raise RuntimeError("The lib 'rarfile' is needed for the un_rar operation!")

    src_path, dst_dir_path = _decompress_check(src, dst_dir)
    with rarfile.RarFile(src_path, "r") as rar_file:
        try:
            if pattern is None:
                matched_inner_files = rar_file.namelist()
            else:
                matched_inner_files = [inner_file for inner_file in rar_file.namelist()
                                       if is_match(pattern, inner_file)]
                rar_file.extractall(dst_dir, matched_inner_files, password)
        except rarfile.RarCannotExec:
            raise FileNotFoundError("Cannot find the UnRAR command line tool!")
        else:
            if delete_src:
                delete(src_path)
        return [str(dst_dir_path.resolve() / inner_file) for inner_file in matched_inner_files]


def un_7z(src: AnyPathLike, dst_dir: AnyPathLike, *, pattern: Optional[str] = None,
          password: Optional[str] = None, delete_src: bool = False) -> List[str]:
    # Attention: the python lib 'py7zr' is needed.
    if py7zr is None:
        raise RuntimeError("The lib 'py7zr' is needed for the un_7z operation!")

    src_path, dst_dir_path = _decompress_check(src, dst_dir)
    with py7zr.SevenZipFile(src_path, "r", password=password) as seven_zip_file:
        if pattern is None:
            matched_inner_files = seven_zip_file.getnames()
        else:
            matched_inner_files = [inner_file for inner_file in seven_zip_file.getnames()
                                   if is_match(pattern, inner_file)]
        seven_zip_file.extract(dst_dir, matched_inner_files)
        if delete_src:
            delete(src_path)
        return [str(dst_dir_path.resolve() / inner_file) for inner_file in matched_inner_files]


def un_tar(src: AnyPathLike, dst_dir: AnyPathLike, *, pattern: Optional[str] = None,
           compression: Optional[str] = None, delete_src: bool = False) -> List[str]:
    src_path, dst_dir_path = _decompress_check(src, dst_dir)
    with tarfile.open(src_path, _get_tar_mode(src_path, "r", compression)) as tar_file:
        if pattern is None:
            matched_inner_members = tar_file.getmembers()
        else:
            matched_inner_members = [member for member in tar_file.getmembers()
                                     if is_match(pattern, member.name)]
        tar_file.extractall(dst_dir, matched_inner_members)
        if delete_src:
            delete(src_path)
        return [str(dst_dir_path.resolve() / inner_member.name) for inner_member in matched_inner_members]


def un_gz(src: AnyPathLike, dst_dir: AnyPathLike, *, delete_src: bool = False) -> str:
    src_path, dst_dir_path = _decompress_check(src, dst_dir)
    with gzip.GzipFile(src_path, "rb") as gz_file:
        output_file_path = dst_dir_path / src_path.with_suffix("").name
        with open(output_file_path, "wb+") as output_file:
            output_file.write(gz_file.read())

    if delete_src:
        delete(src_path)
    return str(output_file_path.resolve())


def un_bz2(src: AnyPathLike, dst_dir: AnyPathLike, *, delete_src: bool = False) -> str:
    src_path, dst_dir_path = _decompress_check(src, dst_dir)
    with bz2.BZ2File(src_path, "rb") as bz_file:
        output_file_path = dst_dir_path / src_path.with_suffix("").name
        with open(output_file_path, "wb+") as output_file:
            output_file.write(bz_file.read())

    if delete_src:
        delete(src_path)
    return str(output_file_path.resolve())


def un_xz(src: AnyPathLike, dst_dir: AnyPathLike, *, delete_src: bool = False) -> str:
    src_path, dst_dir_path = _decompress_check(src, dst_dir)
    with lzma.LZMAFile(src_path, "rb") as xz_file:
        output_file_path = dst_dir_path / src_path.with_suffix("").name
        with open(output_file_path, "wb+") as output_file:
            output_file.write(xz_file.read())

    if delete_src:
        delete(src_path)
    return str(output_file_path.resolve())


def _compress_check(src: MultiPathLike, dst: AnyPathLike) -> Tuple[List[Path], Path]:
    src_path_list = to_multi_path(src)
    dst_path = to_path(dst)
    if is_empty(src_path_list):
        raise ValueError("Source file path cannot be empty!")

    for src_path in src_path_list:
        if not src_path.exists():
            raise IOError(f"Source file {src_path.name} does not exist!")
    if dst_path.is_dir():
        raise IOError(f"Destination path {dst_path.name} already exists and it is a directory!")
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    return src_path_list, dst_path


def _decompress_check(src: AnyPathLike, dst_dir: AnyPathLike) -> Tuple[Path, Path]:
    src_path = to_path(src)
    dst_dir_path = to_path(dst_dir)
    if not src_path.exists():
        raise IOError(f"Source file {src_path.name} does not exist!")
    if not src_path.is_file():
        raise IOError(f"Source path {src_path.name} is a directory!")
    if dst_dir_path.exists() and not dst_dir_path.is_dir():
        raise IOError(f"Destination path {dst_dir_path.name} already exists but it is not a directory!")
    dst_dir_path.mkdir(parents=True, exist_ok=True)
    return src_path, dst_dir_path


def _get_tar_mode(path: Path, mode: str, compression: Optional[str] = None) -> str:
    suffixes = "".join(path.suffixes)
    if compression is None:
        if is_match(r"\.tar", suffixes):
            compression = ""
        elif is_match(r"\.(tar\.gz|tgz)", suffixes):
            compression = "gz"
        elif is_match(r"\.(tar\.xz|txz)", suffixes):
            compression = "xz"
        elif is_match(r"\.(tar\.bz2|tbz|tbz2|tb2)", suffixes):
            compression = "bz2"
        else:
            raise ValueError(f"{suffixes} is not a valid tar file!")
    return f"{mode}:{compression}"
