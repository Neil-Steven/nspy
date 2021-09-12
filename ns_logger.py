#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/6/29
# @Author: Neil Steven

import logging
import sys
import threading
import traceback
from abc import ABCMeta, abstractmethod
from enum import Enum
from logging import handlers
from pathlib import Path
from types import TracebackType
from typing import Optional, Union, Tuple, Any

from ns_unit import parse_humanized_file_size

__all__ = [
    "LogLevel", "LogFormat",
    "NoneLogger", "ConsoleLogger", "FileLogger", "RotatingFileLogger", "TimeRotatingFileLogger"
]

SEPARATOR = " | "
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_SysExcInfoType = Union[Tuple[type, BaseException, Optional[TracebackType]], Tuple[None, None, None]]
_ExcInfoType = Union[None, bool, _SysExcInfoType, BaseException]


class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARNING
    ERROR = logging.ERROR
    FATAL = logging.CRITICAL


_level_to_name = {
    logging.DEBUG: LogLevel.DEBUG,
    logging.INFO: LogLevel.INFO,
    logging.WARNING: LogLevel.WARN,
    logging.ERROR: LogLevel.ERROR,
    logging.CRITICAL: LogLevel.FATAL
}


class _LogFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = _level_to_name[record.levelno].name
        return super().format(record)


# noinspection SpellCheckingInspection
class LogFormat(Enum):
    FULL = _LogFormatter(
        "%(asctime)s.%(msecs)03d" + SEPARATOR
        + "%(module)s:%(funcName)s:%(lineno)d" + SEPARATOR
        + "%(process)d" + SEPARATOR
        + "%(thread)d" + SEPARATOR
        + "%(levelname)s" + SEPARATOR
        + "%(message)s",
        datefmt=DATE_FORMAT
    )
    STANDARD = _LogFormatter(
        "%(asctime)s.%(msecs)03d" + SEPARATOR
        + "%(module)s:%(lineno)d" + SEPARATOR
        + "%(levelname)s" + SEPARATOR
        + "%(message)s",
        datefmt=DATE_FORMAT
    )
    SIMPLE = _LogFormatter(
        "%(asctime)s.%(msecs)03d" + SEPARATOR
        + "%(levelname)s" + SEPARATOR
        + "%(message)s",
        datefmt=DATE_FORMAT
    )
    SHORT = _LogFormatter("%(levelname)s" + SEPARATOR + "%(message)s")
    NONE = _LogFormatter("%(message)s")


class _AbstractLogger(metaclass=ABCMeta):

    @abstractmethod
    def debug(self, message: Any, exception: Optional[_ExcInfoType] = None):
        raise NotImplementedError("Debug function has not been implemented!")

    @abstractmethod
    def info(self, message: Any, exception: Optional[_ExcInfoType] = None):
        raise NotImplementedError("Info function has not been implemented!")

    @abstractmethod
    def warn(self, message: Any, exception: Optional[_ExcInfoType] = None):
        raise NotImplementedError("Warn function has not been implemented!")

    @abstractmethod
    def error(self, message: Any, exception: Optional[_ExcInfoType] = None):
        raise NotImplementedError("Error function has not been implemented!")

    @abstractmethod
    def fatal(self, message: Any, exception: Optional[_ExcInfoType] = None):
        raise NotImplementedError("Fatal function has not been implemented!")


class NoneLogger(_AbstractLogger):
    """
    This is simply a stdout/stderr stream output other than a real logger, which is good for interface compatibility.
    """

    def __init__(self, mark: bool = False, **kwargs):
        super().__init__(**kwargs)
        self._mark = mark

    def debug(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._print(message, exception)

    def info(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._print(message, exception)

    def warn(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._print(message, exception)

    def error(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._print(message, exception, file=sys.stderr)

    def fatal(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._print(message, exception, file=sys.stderr)

    def _print(self, message: Any, exception: Optional[_ExcInfoType] = None, **kwargs):
        # noinspection PyProtectedMember
        mark = f"[{sys._getframe().f_back.f_code.co_name.upper() if self._mark is True else ''}] "
        print(f"{mark}{message}", **kwargs)
        if exception is not None:
            if isinstance(exception, BaseException):
                exc_info = (type(exception), exception, exception.__traceback__)
            else:
                exc_info = sys.exc_info()
            traceback.print_exception(*exc_info, **kwargs)


class _BaseLogger(_AbstractLogger, metaclass=ABCMeta):

    def __init__(self,
                 name: Optional[str] = None,
                 level: LogLevel = LogLevel.INFO,
                 fmt: LogFormat = LogFormat.STANDARD,
                 **kwargs):
        super().__init__(**kwargs)
        self._level = level
        self._format = fmt
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level.value)
        self._lock = threading.RLock()

    @property
    def enable(self) -> bool:
        return not self._logger.disabled

    @enable.setter
    def enable(self, value: bool):
        self._logger.disabled = not value

    @property
    def level(self) -> LogLevel:
        return self._level

    @level.setter
    def level(self, new_level: LogLevel):
        self._acquire_lock()
        self._logger.setLevel(new_level.value)
        for handler in self._logger.handlers:
            handler.setLevel(new_level.value)
        self._level = new_level
        self._release_lock()

    @property
    def format(self) -> LogFormat:
        return self._format

    @format.setter
    def format(self, new_format: LogFormat):
        self._acquire_lock()
        for handler in self._logger.handlers:
            handler.setFormatter(new_format.value)
        self._format = new_format
        self._release_lock()

    def debug(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._logger.debug(message, exc_info=exception, stacklevel=2)

    def info(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._logger.info(message, exc_info=exception, stacklevel=2)

    def warn(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._logger.warning(message, exc_info=exception, stacklevel=2)

    def error(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._logger.error(message, exc_info=exception, stacklevel=2)

    def fatal(self, message: Any, exception: Optional[_ExcInfoType] = None):
        self._logger.critical(message, exc_info=exception, stacklevel=2)

    def _add_handler(self, handler: logging.Handler):
        self._acquire_lock()
        self._logger.addHandler(handler)
        self._refresh_handlers()
        self._release_lock()

    def _remove_handler(self, handler: logging.Handler):
        self._acquire_lock()
        self._logger.removeHandler(handler)
        self._refresh_handlers()
        self._release_lock()

    def _refresh_handlers(self):
        self._acquire_lock()
        for handler in self._logger.handlers:
            handler.setLevel(self.level.value)
            handler.setFormatter(self.format.value)
        self._release_lock()

    def _acquire_lock(self):
        if self._lock:
            self._lock.acquire()

    def _release_lock(self):
        if self._lock:
            self._lock.release()


class ConsoleLogger(_BaseLogger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        stdout_filter = logging.Filter()
        stdout_filter.filter = lambda record: record.levelno < LogLevel.ERROR.value
        self._stdout_handler = logging.StreamHandler(sys.stdout)
        self._stdout_handler.addFilter(stdout_filter)

        stderr_filter = logging.Filter()
        stderr_filter.filter = lambda record: record.levelno >= LogLevel.ERROR.value
        self._stderr_handler = logging.StreamHandler(sys.stderr)
        self._stderr_handler.addFilter(stderr_filter)

        self._add_std_output_handlers()

    def _add_std_output_handlers(self):
        self._acquire_lock()
        self._add_handler(self._stdout_handler)
        self._add_handler(self._stderr_handler)
        self._release_lock()

    def _remove_std_output_handlers(self):
        self._acquire_lock()
        self._remove_handler(self._stdout_handler)
        self._remove_handler(self._stderr_handler)
        self._release_lock()


class _AbstractFileLogger(ConsoleLogger, metaclass=ABCMeta):

    def __init__(self, filename: str = "run.log", enable_console_output: bool = True, **kwargs):
        super().__init__(**kwargs)
        self._filename = filename
        self._enable_console_output = enable_console_output
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        if enable_console_output:
            self._add_std_output_handlers()
        else:
            self._remove_std_output_handlers()

    @property
    def enable_console_output(self) -> bool:
        return self._enable_console_output

    @enable_console_output.setter
    def enable_console_output(self, value: bool):
        self._acquire_lock()
        if self._enable_console_output != value:
            if self._enable_console_output:
                self._remove_std_output_handlers()
            else:
                self._add_std_output_handlers()
            self._enable_console_output = value
        self._release_lock()


class FileLogger(_AbstractFileLogger):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._file_handler = logging.FileHandler(self._filename)
        self._add_handler(self._file_handler)


class RotatingFileLogger(_AbstractFileLogger):

    def __init__(self, max_size: Union[int, str] = "10MiB", backup_count: int = 100, **kwargs):
        if isinstance(max_size, int):
            max_bytes = max_size
        elif isinstance(max_size, str):
            max_bytes = parse_humanized_file_size(max_size)
        else:
            raise ValueError(f"'{max_size}' is not a valid max size!")

        super().__init__(**kwargs)
        self._file_handler = handlers.RotatingFileHandler(self._filename, "a", max_bytes, backup_count)
        self._add_handler(self._file_handler)


class TimeRotatingFileLogger(_AbstractFileLogger):

    def __init__(self, when: str = "H", interval: int = 1, backup_count: int = 100, **kwargs):
        super().__init__(**kwargs)
        self._file_handler = handlers.TimedRotatingFileHandler(self._filename, when, interval, backup_count)
        self._add_handler(self._file_handler)
