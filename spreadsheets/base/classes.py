"""
This file provides all basic classes for using in the library.

class _Address: used to represent addresses in a spreadsheets
class _Cell: represents a singular cell in a spreadsheets
"""


__all__ = [
    'Cell',
    'Address'
]


from typing import Self, Literal
from ..libs.utils import LiteralTypesExt, CellValues


type PositiveInteger = int
type EmptyLiteral = Literal['']


class Address:
    """Representation of address in spreadsheets
    """
    __slots__ = ['__row', '__col', '__value', '__spreadsheets_limits']
    # define in order of all letters,
    # changing this though won't affect functionality,
    # as nothing references to this var
    valid_chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base: int = len(valid_chars)

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
            col_num: int = col_num * cls.base + (ord(char) - ord('A') + 1)
        return col_num

    @classmethod
    def is_valid_col(cls, col:  str) -> bool:
        for char in col:
            if char not in cls.valid_chars:
                return False
        return True

    @classmethod
    def iterate_cols_until(cls, stop_col: str | int) -> list[str]:
        """
        Iterates all columns until it reaches the stop column.
        The stop column will be included as well.
        """
        cols_list: list[str] = []
        col_num = 0

        while True:
            col_num += 1
            col: str = cls.get_col_by_num(col_num)

            cols_list.append(col)

            if isinstance(stop_col, str):
                if col == stop_col:
                    break
            else:
                if col_num == stop_col:
                    break

        return cols_list

    @classmethod
    def split_address_str(cls, address_str: str) -> tuple[str, int]:
        """Splits the string representation of an address into tuple, where first is col, and second is row
        """
        for index, char in enumerate(address_str):
            if char.isdigit():
                return (address_str[:index], int(address_str[index:]))
        return ('', 0)

    @classmethod
    def is_valid_address_str(cls, address_str: str, max_address: tuple[str, int] | None) -> bool:
        """Checks whether address in a format of str is valid or not. Used primarily externally

        Args:
            address_str (str): String representation of an address
            max_address (tuple[str, int]): The corner cell in a spreadsheets. 
                Must be provided as a tuple with [str = 'col', int = 'row']
        """
        col, row = cls.split_address_str(address_str)

        if not cls.is_valid_col(col):
            return False
        
        if col == '' or row == 0:
            return False
        
        if max_address is not None:
            if cls.get_col_num(col) > cls.get_col_num(max_address[0]):
                return False

            if row > max_address[1]:
                return False

        return True

    def __new__(cls, col: str, row: int, spreadsheets_limits: dict[str, int]) -> Self:
        instance: Self = super().__new__(cls)

        if not cls.is_valid_col(col):
            raise NameError(f"Can't name address {col}{row}")

        if cls.get_col_num(col) > spreadsheets_limits['col']:
            raise NameError(f"Can't name address {col}{row}, as it is out of column limit")

        if row > spreadsheets_limits['row']:
            raise NameError(f"Can't name address {col}{row}, as it is out of row limit")

        return instance

    def __init__(self, col: str, row: int, spreadsheets_limits: dict[str, int]) -> None: # type: ignore
        self.__col: str = col
        self.__row: int = row
        self.__value: str = f"{col}{row}"

    @property
    def col(self) -> str:
        return self.__col
    @property
    def n_col(self) -> int:
        return self.get_col_num(self.__col)
    @property
    def row(self) -> int:
        return self.__row

    def __str__(self) -> str:
        return self.__value

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Address):
            raise NotImplementedError("Cannot compare Address with anything than another instance of Address")

        return (self.col == value.col) and (self.row == value.row)

    def __hash__(self) -> int:
        return hash((self.__col, self.__row))

class Cell:
    """Representation of cells
    """
    __slots__ = ['__address', '__type', '__value', '__font_color', '__back_color']

    def __new__(cls, address: Address, cell_type: LiteralTypesExt, value: CellValues) -> Self:
        if not isinstance(value, cell_type):
            raise ValueError(f"The value provided is not of type {cell_type.__name__}")

        return super().__new__(cls)

    def __init__(self, address: Address, cell_type: LiteralTypesExt, value: CellValues) -> None:
        self.__address: Address = address
        self.__type = cell_type
        self.__value = value

    def value(self, new_value: CellValues | None = None) -> CellValues | None:
        """Returns or sets a new value to self.__value

        Args:
            new_value (CellValues, optional): the new value for _Cell.__value. Defaults to None.

        Raises:
            TypeError: if the new value is not one of CellValues

        Returns:
            CellValues | None: Return CellValues if no parameter is provided.
                                Return None if parameter was provided
                                and sets the value of _Cell.__value to the new value (from parameter).
        """
        if new_value is None:
            return self.__value

        self.__value = new_value

    @property
    def address(self) -> Address:
        return self.__address

    def __str__(self) -> str:
        return str(self.__value)

    def __repr__(self) -> str:
        return f"{self.__address}: {self.__value} of type {self.__type.__name__}"
