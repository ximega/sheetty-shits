"""
The library that contains Integer type
"""


__all__ = [
    'Integer',
]



import datetime


class Integer:
    __slots__ = ['__value', '__creation_time', '__id']
    __last_id = 0

    def __init__(self, value: int):
        self.__value = value
        self.__creation_time = datetime.datetime.now()
        Integer.__last_id += 1
        self.__id = Integer.__last_id

    def direct_value(self) -> int:
        return self.__value

    def __str__(self) -> str:
        return str(self.__value)

    def __repr__(self) -> str:
        return f"<Integer> \
            value: {self.__value}, \
            creation_time: {self.__creation_time}, \
            id: {self.__id}"
