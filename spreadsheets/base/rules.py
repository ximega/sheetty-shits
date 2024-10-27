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
    # the commands are defined as following
    # first: command name
    # second: allowed args for a command, that start with single dash (-)
    # third: allowed args for a command, that start with double dash (--)
    Nil = { # type: ignore
        'name': '',
        'argc': [],
        'argv': [],
        'params': range(0, 1)
    }
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
        'param_req': range(0, 1)
    }
    Col = { # type: ignore
        'name': 'col',
        'argc': [],
        'argv': [],
        'param_req': range(2, 3)
    }
    Select = {
        'name': 'select',
        'argc': ['-1', '-2'],
        'argv': ['--l', '--r', '--u', '--d'],
        'param_req': range(1, 11)
    }
    Deselect = { # type: ignore
        'name': 'deselect',
        'argc': [],
        'argv': [],
        'param_req': range(0, 1)
    }

    def __getitem__(self, name: str) -> str | list[str] | range:
        return self.value[name] # type: ignore

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.value['name'] == other # type: ignore
        elif isinstance(other, Commands):
            return self.value['name'] == other.value['name'] # type: ignore

        raise TypeError(f"Cannot compare Commands with {other.__class__.__name__}")

    def __str__(self) -> str:
        return self.value['name'] # type: ignore

class ExecutionCommands(Enum):
    Select = auto

class SelectFormats(Enum):
    Nil = auto()
    ZeroDim = auto()
    OneDim = auto()
    TwoDim = auto()
    Line = auto()
    Rectangle = auto()

class SelectDirection(Enum):
    Left = auto()
    Right = auto()
    Up = auto()
    Down = auto()