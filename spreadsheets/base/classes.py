__all__ = [
    'Spreadsheets',
    '_Address'
]



import math
from ..libs import _CellValues
from ..libs.utils import _LiteralTypes
from typing import Self


type PositiveInteger = int

class _Address:
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    @classmethod
    def get_col_by_num(cls, num: int) -> str:
        cnum = num
        col = str()
        highest_power: int = math.floor(math.log(cnum, 26))
        for power in range(highest_power, -1, -1):
            power_of_26 = 26**power
            char_index = cnum // power_of_26
            cnum -= char_index * power_of_26
            if cnum == 0 and num > 26:
                char_index += 1
                cnum += power_of_26
            col += cls.valid_chars[char_index-1]
        return col
        
    @classmethod
    def get_col_num(cls, col: str) -> str:
        col_num = 1
        for index, char in enumerate(col[::-1]):
            col_num += (cls.valid_chars.index(char)+1) * 26**(index)
    
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
        self.col = col
        self.row = row
        self.value = f"{col}{row}"
        
    def __str__(self) -> str:
        return f"{self.col}{self.row}"

class _Cell:
    def __init__(self, address: _Address, type: _LiteralTypes, value: _CellValues):
        pass

class Spreadsheets:
    def __init__(self, *,
            dynamic: bool = False, 
            char_width: PositiveInteger = 7, 
            col_max: PositiveInteger = 1000,
            row_max: PositiveInteger = 1000, 
        ):
        
        self.__dynamic = dynamic
        self.__char_width = char_width
        self.__limits = {'col': col_max, 'row': row_max}
        self.__content = {}
        
    def printf(self) -> str:
        return ''
        
    def run(self) -> None:
        if not self.dynamic:
            raise PermissionError("Spreadsheets are not dynamic, can't use .run() method")