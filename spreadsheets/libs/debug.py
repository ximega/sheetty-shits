"""
Adds functionality for debugging libraries
"""


__all__ = [
    '_Debugger',
]


class _Debugger:
    """
    Class that allows to create an instance of debug object inside other libraries for debugging
    """
    __slots__ = ['__obj']

    def __init__(self, obj) -> None:
        self.__obj = obj

    def list_int_values(self) -> list[int]:
        """
        Designed for libs.Array and libs.Multiple
        to list their .__values, if type is set to Integer
        """
        return [x.direct_value() for x in self.__obj.values()]