"""This module contains all rules
that an user might use
to change styles, formats and etc. in the spreadsheets
"""


from enum import Enum, auto


class DfTime(Enum):
    H24 = auto()
    H12 = auto()
    FSTR = auto()
    STR = auto()

class DfDate(Enum):
    DEFAULT = auto()
    EN_US = auto()

class DfDateMonth(Enum):
    INT = auto()
    STR = auto()
    FSTR = auto()

class DfDateYear(Enum):
    CHAR2 = auto()
    CHAR4 = auto()

class DfPreciseTime(Enum):
    FSTR = auto()
    STR = auto()
    INT = auto()

class DfDateTime(Enum):
    FSTR = auto()
    STR = auto()
    INT = auto()
    FULL_STR = auto()

class RegDateTime(Enum):
    DEFAULT = auto()
    US = auto()