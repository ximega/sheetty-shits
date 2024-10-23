"""
The library that contains Multiple type
"""


__all__ = [
    'Multiple',
]



import datetime
from typing import Self
from .array import Array
from .integer import Integer
from .string import String
from ..libs.debug import Debugger


type _LiteralTypes = type[String] | type[Integer] | type[Array]
type _CellValues = String | Integer | Array


class Multiple:
    """
    Multiple-choice cell. Displays current value by default
    Has ability to be changed, from values that it contain
    """
    __slots__ = ['__type', '__current_value', '__values', '__creation_time', '__id', 'debugger']
    __last_id = 0

    def __new__(cls, multiple_type: _LiteralTypes, values: list[_CellValues]) -> Self:
        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, multiple_type: _LiteralTypes, values: list[_CellValues]):
        self.__type = multiple_type
        self.__current_value: _CellValues | None = None
        self.__values = values
        self.__creation_time = datetime.datetime.now()
        self.__id = self.__last_id
        self.debugger = Debugger(self)

    def values(self) -> list[_CellValues]:
        return self.__values

    def choose(self, index: int) -> None:
        """Changes Multiple.__current_value

        Args:
            index (int): the index of value for Multiple.__current_value to be changed to

        Raises:
            ValueError: if there is no value at the specified index
        """
        try:
            self.__current_value = self.__values[index]
        except IndexError as exc:
            raise ValueError(f"There is no element at index {index} in this Multiple-choice cell") from exc

    def expand(self, *new_values: _CellValues) -> None:
        """Expands the list of values

        Args:
            *new_values (_CellValues): all values that a user wants to add to Multiple.__values
        """
        self.__values.extend(new_values)

    def remove(self, index: int) -> None:
        """Removes an element at index

        Args:
            index (int): the index at which element is placed
        """
        self.__values.pop(index)

    def reposition(self, item_index: int, new_index: int) -> None:
        """Moves a value to a particular index. Increases the index of values under.

        Args:
            item_index (int): the index of value that want to be repositioned
            new_index (int): the index at which the item will be
        """
        item = self.__values[item_index]
        self.__values.pop(item_index)

        self.__values.insert(new_index, item)

    def __str__(self) -> str:
        return str(self.__current_value)

    def __repr__(self) -> str:
        return f"<Multiple<{self.__type.__name__}>> \
            \nvalues: {self.__values}, \
            \ncurrent_value: {self.__current_value}, \
            \ncreation_time: {self.__creation_time}, \
            \nid: {self.__id}"
