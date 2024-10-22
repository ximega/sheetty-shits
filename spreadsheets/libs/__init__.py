"""
spreadsheets.libs contain all libraries that can be used in the spreadsheets.

Most command libraries:
 - Value types: array, integer, multiple, string, float
 - Utilities: utils
 - Additional types: time (time & date)
"""


__all__ = [
    'String',
    'Array',
    'Integer',
    'Float',
    'Null'
]


from typing import Self

from .string import String
from .integer import Integer
from .array import Array
from .float import Float


class _NullType:
    """
    Type for only instance of Null.
    New instances cannot be created from this object
    """
    __slots__ = []
    __instanced = False

    def __new__(cls) -> Self:
        if cls.__instanced:
            raise PermissionError("Cannot create another instance of _NullType")

        return super().__new__(cls)

    def __str__(self) -> str:
        return 'NULL'

    def __repr__(self) -> str:
        return 'NULL'

Null = _NullType()
