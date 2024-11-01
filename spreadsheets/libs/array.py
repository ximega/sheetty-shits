"""
The library that contains Array type
"""


__all__ = [
    'Array',
]



import datetime
from typing import Any, Self
from .string import String
from .integer import Integer
from .float import Float
from .debug import Debugger


type _LiteralTypes = type[String] | type[Integer] | type[Float]
type _CellTypes = String | Integer | Float


class Array:
    __slots__ = ['__type', '__values', '__creation_time', '__id', 'debugger']
    __last_id = 0

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, array_type: _LiteralTypes, values: list[_CellTypes]) -> None:
        self.__type = array_type
        self.__values: list[String | Integer | Float] = values
        self.__creation_time: datetime.datetime = datetime.datetime.now()
        self.__id: int = self.__last_id
        self.debugger = Debugger(self)

    @property
    def values(self):
        return self.__values
    
    def append(self, value: _CellTypes) -> None:
        """Adds a new value to an Array"""
        if not isinstance(value, self.__type):
            raise TypeError(f"The value provided must be of type {self.__type.__name__}")
        self.__values.append(value)

    def remove(self, index_or_value: int | _CellTypes) -> None:
        """Removes an element from an Array
        """
        if (not isinstance(index_or_value, int)) and (not isinstance(index_or_value, self.__type)):
            raise TypeError

        if isinstance(index_or_value, int):
            self.__values.pop(index_or_value)
        else:
            self.__values.remove(index_or_value)

    def __str__(self) -> str:
        return '* ' + ", ".join([str(x) for x in self.__values])

    def __repr__(self) -> str:
        return f"<Array<{self.__type.__name__}>> \
            \nvalues: {self.__values}, \
            \ncreation_time: {self.__creation_time}, \
            \nid: {self.__id}"
