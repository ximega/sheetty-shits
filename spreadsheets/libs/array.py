"""
The library that contains Array type
"""


__all__ = [
    'Array',
]



import datetime
from typing import Self
from .string import String
from .integer import Integer
from .debug import _Debugger


type _LiteralTypes = type[String] | type[Integer]


class Array:
    __slots__ = ['__type', '__values', '__creation_time', '__id', 'debugger']
    __last_id = 0

    def __new__(cls, *args, **kwargs) -> Self:
        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, array_type: _LiteralTypes, values: list[String | Integer]):
        self.__type = array_type
        self.__values = values
        self.__creation_time = datetime.datetime.now()
        self.__id = self.__last_id
        self.debugger = _Debugger(self)

    def values(self) -> list[String | Integer]:
        return self.__values

    def __str__(self) -> str:
        return ", ".join([str(x) for x in self.__values])

    def __repr__(self) -> str:
        return f"<Array<{self.__type.__name__}>> \
            \nvalues: {self.__values}, \
            \ncreation_time: {self.__creation_time}, \
            \nid: {self.__id}"
