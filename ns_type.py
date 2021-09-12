#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2021/7/15
# @Author: Neil Steven

from typing import TypeVar, Generic, Type, Any, final, Optional

from ns_datetime import DEFAULT_DATE_FORMAT, timestamp_to_date, date_to_timestamp

__all__ = [
    "Typed",
    "TypedInt", "TypedFloat", "TypedBool", "TypedComplex", "TypedStr",
    "TypedList", "TypedTuple", "TypedSet", "TypedDict",
    "TypedDate", "TypedTimestamp"
]

T = TypeVar("T")


class Typed(Generic[T]):
    __slots__ = ("_name", "_expected_type", "_default_value", "_strict")

    def __init__(self, expected_type: Type[T], default_value: T = None, strict: bool = False):
        self._expected_type = expected_type
        self._default_value = default_value
        self._strict = strict

    @property
    def expected_type(self) -> T:
        return self._expected_type

    @property
    def default_value(self) -> T:
        return self._default_value

    @property
    def strict(self) -> T:
        return self._strict

    @final
    def convert(self, value: Any) -> T:
        try:
            return self._do_convert(value)
        except BaseException:
            raise TypeError(f"Failed to convert {value} to {self._expected_type}!")

    def _do_convert(self, value: Any) -> T:
        return self._expected_type(value)

    def __get__(self, instance, owner) -> T:
        if instance is None:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, self._expected_type):
            if self._strict:
                raise TypeError(f"Expected type {self._expected_type}, got {type(value)}")
            else:
                value = self.convert(value)
        instance.__dict__[self._name] = value

    def __delete__(self, instance):
        del instance.__dict__[self._name]

    def __set_name__(self, owner, name):
        self._name = name


class TypedInt(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = int
        super().__init__(**kwargs)


class TypedFloat(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = float
        super().__init__(**kwargs)


class TypedBool(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = bool
        super().__init__(**kwargs)


class TypedComplex(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = complex
        super().__init__(**kwargs)


class TypedStr(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = str
        super().__init__(**kwargs)


class TypedList(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = list
        super().__init__(**kwargs)


class TypedTuple(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = tuple
        super().__init__(**kwargs)


class TypedSet(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = set
        super().__init__(**kwargs)


class TypedDict(Typed):
    def __init__(self, **kwargs):
        kwargs["expected_type"] = dict
        super().__init__(**kwargs)


class TypedDate(TypedStr):
    def __init__(self, fmt: str = DEFAULT_DATE_FORMAT, **kwargs):
        self._format = fmt
        super().__init__(**kwargs)

    def _do_convert(self, value: Any) -> T:
        if isinstance(value, int):
            value = timestamp_to_date(value, self._format)
        return super()._do_convert(value)


class TypedTimestamp(TypedInt):
    def __init__(self, string_format: Optional[str] = DEFAULT_DATE_FORMAT, **kwargs):
        self._format = string_format
        super().__init__(**kwargs)

    def _do_convert(self, value: Any) -> T:
        if isinstance(value, str) and self._format is not None:
            value = date_to_timestamp(value, self._format)
        return super()._do_convert(value)
