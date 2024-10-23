"""
This file provides all basic classes for using in the library.

class _Address: used to represent addresses in a spreadsheets
class _Cell: represents a singular cell in a spreadsheets
class Spreadsheets: used to create, delete, and do other manipulations with it
"""


__all__ = [
    'Spreadsheets',
    'Cell',
    'Address'
]



from typing import Self, Literal
from ..libs.utils import LiteralTypesExt, CellValues


type PositiveInteger = int
type EmptyLiteral = Literal['']

EMPTY_SPACE = ' '
V_SEPARATOR = ' | '
H_SEPARATOR = ' ― '
NEW_LINE = '\n'
VERTICAL_RATIO = 2.9


class Address:
    """Representation of address in spreadsheets
    """
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
    def __get_col_num(cls, col: str) -> int:
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

    def __new__(cls, col: str, row: int, spreadsheets_limits: dict[str, int]) -> Self:
        instance = super().__new__(cls)

        for char in col:
            if char not in cls.valid_chars:
                raise NameError(f"Can't name address {col}{row}")

        if cls.__get_col_num(col) > spreadsheets_limits['col']:
            raise NameError(f"Can't name address {col}{row}, as it is out of column limit")

        if row > spreadsheets_limits['row']:
            raise NameError(f"Can't name address {col}{row}, as it is out of row limit")

        return instance

    def __init__(self, col: str, row: int, spreadsheets_limits: dict[str, int]) -> None:
        self.__col = col
        self.__row = row
        self.__value = f"{col}{row}"

    @property
    def col(self) -> str:
        return self.__col
    @property
    def n_col(self) -> int:
        return self.__get_col_num(self.__col)
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
    __slots__ = ['__address', '__type', '__value']

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

class Spreadsheets:
    """
    Class for instantiating a new spreadsheets table
    """
    __slots__ = ['__dynamic', '__char_width', '__limits', '__content', '__max_address']

    def __new__(cls, *,
            dynamic: bool = False,
            char_width: PositiveInteger = 7,
            col_max: PositiveInteger = 1000,
            row_max: PositiveInteger = 1000,
        ) -> Self:

        return super().__new__(cls)

    def __init__(self, *,
            dynamic: bool = False,
            char_width: PositiveInteger = 7,
            col_max: PositiveInteger = 1000,
            row_max: PositiveInteger = 1000,
        ) -> None:

        self.__dynamic: bool = dynamic
        self.__char_width: PositiveInteger = char_width
        self.__limits: dict[str, int] = {'col': col_max, 'row': row_max}
        self.__content: dict[Address, Cell] = {}
        self.__max_address: Address | None = None

    def limits_dict(self) -> dict[str, int]:
        """Returns limits as a dict
        """
        return self.__limits

    def limits(self) -> str:
        """Gives information about spreadsheets limits
        """
        return f"col: {self.__limits['col']}\nrow: {self.__limits['row']}"

    def __corner_address(self) -> Address:
        """Return the most bottom and right value in the spreadsheets.
        Used to find the width and height for formatting spreadsheets

        Returns:
            _Cell: the cell that is in corner.
        """
        if self.__max_address is None:
            raise ValueError("Spreadsheets are empty. Cannot use corner_value method")

        return self.__max_address

    def __try_settings_new_max_cell(self, address: Address) -> None:
        if self.__max_address is None:
            self.__max_address = address
            return

        if (address.n_col > self.__max_address.n_col) and (address.row > self.__max_address.row):
            self.__max_address = address
            return
        elif (address.n_col > self.__max_address.n_col) and (address.row < self.__max_address.row):
            self.__max_address = Address(Address.get_col_by_num(address.n_col), self.__max_address.row, self.__limits)
            return
        elif (address.n_col < self.__max_address.n_col) and (address.row > self.__max_address.row):
            self.__max_address = Address(self.__max_address.col, address.row, self.__limits)

    def add(self, cell: Cell) -> None:
        """Adds an object to the contents of a spreadsheets

        Args:
            cell (Cell): the object of Cell that is wanted to be put at a particular address

        Raises:
            ValueError: If there is already an object at the address of the cell
        """
        if cell.address in self.__content:
            raise ValueError("There is already an object at the address")

        self.__content[cell.address] = cell

        self.__try_settings_new_max_cell(cell.address)

    def printf(self) -> None:
        """Formats and prints spreadsheets to a console

        Returns:
            str: the formatted spreadsheets
        """
        formatted = str()

        max_col: str = self.__corner_address().col
        max_row: int = self.__corner_address().row

        row_len: int = len(str(max_row))

        cols = Address.iterate_cols_until(max_col)


        # first line with columns
        formatted += EMPTY_SPACE*row_len

        for col in cols:
            rest_space = self.__char_width - len(col)
            formatted += V_SEPARATOR + col + EMPTY_SPACE*rest_space

        # second (and others as well) line separators
        v_separators = H_SEPARATOR * (int(len(formatted)/VERTICAL_RATIO))

        # main values
        for row in range(1, max_row+1):
            formatted += NEW_LINE
            formatted += v_separators
            formatted += NEW_LINE

            rest_space = row_len - len(str(row))
            formatted += str(row) + EMPTY_SPACE*rest_space

            for col in cols:
                address = Address(col, row, self.__limits)
                value: Cell | Literal[''] | None = None
                try:
                    value = self.__content[address]
                except KeyError:
                    value = ''

                value_len = len(str(value))
                rest_space = self.__char_width - value_len

                formatted += V_SEPARATOR + str(value) + EMPTY_SPACE*rest_space

        print(formatted)

    def run(self) -> None:
        """Runs a dynamic version of spreadsheets with a console for dynamic commands
        """
        if not self.__dynamic:
            raise PermissionError("Spreadsheets are not dynamic, can't use .run() method")

        raise NotImplementedError("The run function is not yet implemented for use")
