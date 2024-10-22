"""
The library that contains Float type
"""


__all__ = [
    'boolFalse',
    'boolTrue',
    'Boolean'
]



import datetime
from typing import Literal, Self


type BooleanLiteral = Literal['TRUE', 'FALSE']

class Boolean:
    """
    Command type for only two boolean types: TRUE and FALSE
    """
    __slots__ = ['__value', '__creation_time', '__id']
    __allowed_values = ['TRUE', 'FALSE']
    __last_id = 0

    def __new__(cls, value: BooleanLiteral) -> Self:
        if value not in cls.__allowed_values:
            raise PermissionError("Cannot instantiate new Boolean type")

        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, value: BooleanLiteral) -> None:
        self.__value = value
        self.__creation_time = datetime.datetime.now()
        self.__id = self.__last_id

    def get_direct_value(self) -> float:
        return self.__value

    def change_value(self, new_value: BooleanLiteral) -> None:
        self.__value = new_value

    def __str__(self) -> str:
        return str(self.__value)

    def __repr__(self) -> str:
        return f"<Boolean> \
            value: {self.__value}, \
            creation_time: {self.__creation_time}, \
            id: {self.__id}"

boolTrue = Boolean('TRUE')
boolFalse = Boolean('FALSE')
