__all__ = [
    'String',
]



import datetime


class String:
    __last_id = 0
    
    def __init__(self, value: str):
        self.__value = value
        self.__creation_time = datetime.datetime.now()
        self.__class__.__last_id += 1
        self.__id = self.__class__.__last_id
    
    def __str__(self) -> str:
        return self.__value
    
    def __repr__(self) -> str:
        return f"<String> value: {self.__value}, create_time: {self.__creation_time}, id: {self.__id}"
    
    