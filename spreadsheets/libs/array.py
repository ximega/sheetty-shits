__all__ = [
    'Array',
]



import datetime
from .string import String
from .integer import Integer


type _LiteralTypes = type[String] | type[Integer]


class Array:
    __slots__ = ['__type', '__values', '__creation_time', '__id']
    __last_id = 0
    
    def __init__(self, array_type: _LiteralTypes, values: list[String | Integer]):
        self.__type = array_type
        self.__values = values
        self.__creation_time = datetime.datetime.now()
        self.__class__.__last_id += 1
        self.__id = self.__class__.__last_id
    
    def __str__(self) -> str:
        return ", ".join([str(x) for x in self.__values])
    
    def __repr__(self) -> str:
        return f"<Array<{self.__type.__name__}>> \nvalues: {self.__values}, \ncreation_time: {self.__creation_time}, \nid: {self.__id}"
    
    