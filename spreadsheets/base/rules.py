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

class Commands(Enum):
    """Contains all commands that are available in dynamic mode
    """
    Nil = auto()
    # the commands are defined as following
    # first: command name
    # second: allowed args for a command, that start with single dash (-)
    # third: allowed args for a command, that start with double dash (--)
    Exit = { # type: ignore
        'name': 'exit',
        'argc': [],
        'argv': [],
        'param_req': range(0, 1)
    }
    Get = { # type: ignore
        'name': 'get',
        'argc': [],
        'argv': [],
        'param_req': range(1, 2)
    }
    Col = { # type: ignore
        'name': 'col',
        'argc': [],
        'argv': [],
        'param_req': range(2, 3)
    }

    def __getitem__(self, name: str) -> str | list[str] | range:
        return self.value[name] # type: ignore

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            raise TypeError(f"Cannot compare Commands with {other.__class__.__name__}")

        return self.value['name'] == other # type: ignore
