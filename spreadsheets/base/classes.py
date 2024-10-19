__all__ = [
    'Spreadsheets',
    '_Address',
    '_Cell'
]



import math
from ..libs import _CellValues
from ..libs.utils import _LiteralTypes, _highest_power_of
from typing import Self


type PositiveInteger = int

class _Address:
    valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # define in order of all letters
    base = len(valid_chars)
    
    @classmethod
    def get_col_by_num(cls, num: PositiveInteger) -> str:
        if num < 1:
            raise ValueError("param 'num' cannot be lower than 1")
        
        # finding all ba
        all_n: list[int] = []
        power = 0
        while True:
            n = cls.base ** power
            if n > num: break
            all_n.append(n)
            power += 1
        
        # finding the column itself
        col = str()
        c_num = num 
        all_n = all_n[::-1]
        for index, n in enumerate(all_n):
            multiplier = c_num // n
            if (multiplier == cls.base + 1):
                multiplier -= 1
            
            mul = n * multiplier
            if (mul == c_num) and (n != 1):
                multiplier -= 1
                    
            char = cls.valid_chars[multiplier-1]
            
            if (char == 'A') and (index != len(all_n)-1):
                next_n = all_n[index+1]
                if next_n != 1:
                    next_multiplier = c_num // next_n
                    if next_multiplier == cls.base+1:
                        continue
            
            col += char
            c_num -= mul
        
        return col
        
    @classmethod
    def get_col_num(cls, col: str) -> int:
        col_num = 0
        for index, char in enumerate(col[::-1]):
            col_num += (cls.valid_chars.index(char)+1) * cls.base**(index)
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