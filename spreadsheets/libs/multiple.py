"""
The library that contains Multiple type
"""


__all__ = [
    'Multiple',
]



import datetime
from .array import Array
from .integer import Integer
from .string import String


type _LiteralTypes = type[String] | type[Integer] | type[Array]
type _CellValues = String | Integer | Array


class Multiple:
    """
    Multiple-choice cell. Displays current value by default
    Has ability to be changed, from values that it contain
    """
    __slots__ = ['__type', '__current_value', '__values', '__creation_time', '__id']
    __last_id = 0

    def __init__(self, multiple_type: _LiteralTypes, values: list[_CellValues]):
        self.__type = multiple_type
        self.__current_value: _CellValues | None = None
        self.__values = values
        self.__creation_time = datetime.datetime.now()
        self.__class__.__last_id += 1
        self.__id = self.__class__.__last_id

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

    def __str__(self) -> str:
        return self.__current_value

    def __repr__(self) -> str:
        return f"<Multiple<{self.__type.__name__}>> \
            \nvalues: {self.__values}, \
            \ncurrent_value: {self.__current_value}, \
            \ncreation_time: {self.__creation_time}, \
            \nid: {self.__id}"