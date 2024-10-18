__all__ = [
    'Array',
]



import datetime
from .string import String
from .integer import Integer
from .utils import _LiteralTypes


class Array:
    __last_id = 0
    
    def __init__(self, types: list[_LiteralTypes], values: list[String | Integer]):
        self.__types = types
        self.__values = values
        self.__creation_time = datetime.datetime.now()
        self.__class__.__last_id += 1
        self.__id = self.__class__.__last_id
    
    def __str__(self) -> str:
        return ", ".join([str(x) for x in self.__values])
    
    def __repr__(self) -> str:
        return f"<Array<{", ".join([x.__name__ for x in self.__types])}>> value: {self.__values}, create_time: {self.__creation_time}, id: {self.__id}"
    
    