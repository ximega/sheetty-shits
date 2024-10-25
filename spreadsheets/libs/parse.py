"""
This lib helps to parse any external into this spreadsheets
"""


__all__ = [
    'Parser'
]


from ..base.classes import Spreadsheets, Address, Cell
from .utils import CellValues
from .string import String


class Parser:
    """Class that combines all types of parsing
    Fills all data into a specified spreadsheets

    NOTE: The parser works only with integers, strings, float values, and arrays of these three types.
    Array must be of one type.
    """

    __slots__ = ['__sp']

    def __init__(self, sp: Spreadsheets) -> None:
        self.__sp: Spreadsheets = sp

    def __str__(self) -> str:
        return "<Parser>"

    def from_dict(self, dct: dict[str, list[CellValues]]) -> Spreadsheets:
        """Formats info from a dict and adds info to the spreadsheets
        """

        for col_n, (key, value) in enumerate(dct.items(), start=1): # type: ignore
            self.__sp.add(
                Cell(
                    Address(Address.get_col_by_num(col_n), 1, self.__sp.limits_dict()),
                    String,
                    String(key)
                )
            )

            for row, item in enumerate(value, start=1):
                self.__sp.add(
                    Cell(
                        Address(Address.get_col_by_num(col_n), row+1, self.__sp.limits_dict()),
                        item.__class__,
                        item
                    )
                )

        return self.__sp

    def from_txt(self, source: str) -> Spreadsheets:
                # implementation for defining types and values of cell in a txt file
                # val_type, val_raw, val = None, None, None

                # try:
                #     # if works it is either Integer or Float
                #     val_raw = int(item)
                # except ValueError:
                #     # if raises error it is either String or Array
        return self.__sp
