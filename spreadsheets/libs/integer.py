"""
The library that contains Integer type
"""


__all__ = [
    'Integer',
]



import datetime
from typing import Self


class Integer:
    __slots__ = ['__value', '__creation_time', '__id']
    __last_id = 0

    def __new__(cls, *args, **kwargs) -> Self:
        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, value: int) -> None:
        self.__value = value
        self.__creation_time = datetime.datetime.now()
        self.__id = self.__last_id

    def get_direct_value(self) -> int:
        return self.__value

    def change_value(self, new_value: int) -> None:
        self.__value = new_value

    def increment(self) -> None:
        self.__value += 1

    def decrement(self) -> None:
        self.__value -= 1

    def __str__(self) -> str:
        return str(self.__value)

    def __repr__(self) -> str:
        return f"<Integer> \
            value: {self.__value}, \
            creation_time: {self.__creation_time}, \
            id: {self.__id}"
