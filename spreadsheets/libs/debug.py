"""
Adds functionality for debugging libraries
"""


__all__ = [
    '_Debugger',
]


class _Debugger:
    """
    Class that allows to create an instance of debug object inside other libraries for debugging

    Methods doesn't have any clear typing annotations 
    as it would cause circular import
    and was decided to leave error-prone code
    """
    __slots__ = ['__obj']

    def __init__(self, obj) -> None:
        self.__obj = obj

    def list_int_values(self) -> list[int]:
        """
        Designed for libs.Array and libs.Multiple
        to list their .__values, if type is set to Integer
        """
        return [x.get_direct_value() for x in self.__obj.values()]
    