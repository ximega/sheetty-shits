"""
This file provides all basic classes for using in the library.

class _Address: used to represent addresses in a spreadsheets
class _Cell: represents a singular cell in a spreadsheets
class Spreadsheets: used to create, delete, and do other manipulations with it
"""


__all__ = [
    'Spreadsheets',
    '_Address',
    '_Cell'
]



from typing import Self
from ..libs.utils import _LiteralTypesExt, _CellValues


type PositiveInteger = int

class _Address:
    __slots__ = ['__row', '__col', '__value', '__spreadsheets_limits']
    # define in order of all letters,
    # changing this though won't affect functionality,
    # as nothing references to this var
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(valid_chars)

    @classmethod
    def get_col_by_num(cls, num: PositiveInteger) -> str:
        """Return column address 

        Args:
            num (PositiveInteger): the order number of the column 
                                   (must include all letters, without any being skipped)

        Returns:
            str: column address (A-Z*[int]), i.e. AZJGS, DG, A, N, ODS
        """
        col = str()
        while num > 0:
            num -= 1
            col += chr(num % cls.base + ord('A'))
            num //= 26
        return col[::-1]

    @classmethod
    def get_col_num(cls, col: str) -> int:
        """Return order number of a column

        Args:
            col (str): column address (A-Z*[int]), i.e. BFD, JD, L, ALD

        Returns:
            int: order number of the column address 
        """
        col_num = 0
        for char in col:
            col_num = col_num * cls.base + (ord(char) - ord('A') + 1)
        return col_num

    def __new__(cls, col: str, row: int, spreadsheets_limits: dict[str, int]) -> Self:
        instance = super().__new__(cls)

        for char in col:
            if char not in cls.valid_chars:
                raise NameError(f"Can't name address {col}{row}")

        if cls.get_col_num(col) > spreadsheets_limits['col']:
            raise NameError(f"Can't name address {col}{row}, as it is out of column limit")

        if row > spreadsheets_limits['row']:
            raise NameError(f"Can't name address {col}{row}, as it is out of row limit")

        return instance

    def __init__(self, col: str, row: int, spreadsheets_limits: tuple[int, int]) -> None:
        self.__col = col
        self.__row = row
        self.__value = f"{col}{row}"
        self.__spreadsheets_limits = spreadsheets_limits

    @property
    def col(self): return self.__col
    @property
    def row(self): return self.__row

    def __str__(self) -> str:
        return self.__value

class _Cell:
    __slots__ = ['__address', '__type', '__value']

    def __new__(cls, address: _Address, cell_type: _LiteralTypesExt, value: _CellValues) -> Self:
        instance = super().__new__(cls)

        if not isinstance(value, cell_type):
            raise ValueError(f"The value provided is not of type {cell_type.__name__}")

        return instance

    def __init__(self, address: _Address, cell_type: _LiteralTypesExt, value: _CellValues) -> None:
        self.__address = address
        self.__type = cell_type
        self.__value = value

    def value(self, new_value: _CellValues = None) -> _CellValues | None:
        """_summary_

        Args:
            new_value (_CellValues, optional): the new value for _Cell.__value. Defaults to None.

        Raises:
            TypeError: if the new value is not one of _CellValues

        Returns:
            _CellValues | None: Return _CellValues if no parameter is provided.
                                Return None if parameter was provided
                                and sets the value of _Cell.__value to the new value (from parameter).
        """
        if new_value is None:
            return self.__value
        elif isinstance(new_value, _CellValues):
            self.__value = new_value
        else:
            raise TypeError("new_value must be of type _CellValues")

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return f"{self.__address}: {self.__value} of type {self.__type.__name__}"

class Spreadsheets:
    """
    Class for instantiating a new spreadsheets table
    """
    __slots__ = ['__dynamic', '__char_width', '__limits', '__content']

    def __init__(self, *,
            dynamic: bool = False,
            char_width: PositiveInteger = 7,
            col_max: PositiveInteger = 1000,
            row_max: PositiveInteger = 1000,
        ) -> None:

        self.__dynamic = dynamic
        self.__char_width = char_width
        self.__limits = {'col': col_max, 'row': row_max}
        self.__content = {}

    @property
    def limits(self):
        return f"col: {self.__limits['col']}\nrow: {self.__limits['row']}"

    def corner_value(self) -> _Cell:
        """Return the most bottom and right value in the spreadsheets.
        Used to find the width and height for formatting spreadsheets
        
        Returns:
            _Cell: the cell that is in corner.
        """ 

    def printf(self) -> str:
        """Formats and prints spreadsheets to a console

        Returns:
            str: the formatted spreadsheets
        """
        return ''

    def run(self) -> None:
        """Runs a dynamic version of spreadsheets with a console for dynamic commands
        """
        if not self.__dynamic:
            raise PermissionError("Spreadsheets are not dynamic, can't use .run() method")