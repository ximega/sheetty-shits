"""
The library that contains String type
"""


__all__ = [
    'String',
]



import datetime
from typing import Self


class String:
    __slots__ = ['__value', '__creation_time', '__id']
    __last_id = 0

    def __new__(cls, value: str) -> Self:
        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, value: str):
        self.__value = value
        self.__creation_time = datetime.datetime.now()
        self.__id = self.__last_id

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return f"<String> \
            value: {self.__value}, \
            creation_time: {self.__creation_time}, \
            id: {self.__id}"
