"""
The library that contains Float type
"""


__all__ = [
    'Float',
]



import datetime


class Float:
    __slots__ = ['__value', '__creation_time', '__id']
    __last_id = 0

    def __init__(self, value: float) -> None:
        self.__value = value
        self.__creation_time = datetime.datetime.now()
        Float.__last_id += 1
        self.__id = Float.__last_id

    def get_direct_value(self) -> float:
        return self.__value

    def change_value(self, new_value: float) -> None:
        self.__value = new_value

    def __str__(self) -> str:
        return str(self.__value)

    def __repr__(self) -> str:
        return f"<Float> \
            value: {self.__value}, \
            creation_time: {self.__creation_time}, \
            id: {self.__id}"
