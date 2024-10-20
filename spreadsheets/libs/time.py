"""
This library contains necessary time-related types, like:
Time (i.e. 14:43)
Date (i.e. 07/12/2024)
TimePeriod (i.e. 5 minutes)
TimeSpan (i.e. 14:55-15:03)
DateSpan (i.e. 04/06/2024-30/06/2024)
PreciseTime (i.e. 06:15:22, 22:04:24:453)
"""


__all__ = [
    'Time',
    'Date',
    'TimePeriod',
    'TimeSpan',
    'DateSpan',
    'PreciseTime',
]



from enum import Enum
from typing import Literal, Self

# df - display format
type df_TimeLiteral = Literal[12, 24]
type df_DateLiteral = Literal['default', 'us']
type df_MonthLiteral = Literal['fstr', 'str', 'int']
type df_YearLiteral = Literal[2, 4]

def _inclusive_range(start: int, stop: int) -> range:
    return range(start, stop+1)

class Time:
    """
    The type represents time in a format: H:m
    """

    __slots__ = ['__id', 'h', 'm', '__display_format', '__strdata']
    __last_id = 0
    __allowed_df_literals = [12, 24]

    def __new__(cls, h: int, m: int, display_format: df_TimeLiteral = 24) -> Self:
        if h not in _inclusive_range(0, 23):
            raise ValueError("Hour must equal any number between 0 and 23")
        if m not in _inclusive_range(0, 59):
            raise ValueError("Minute must equal any number between 0 and 59")
        if display_format not in (12, 24):
            raise ValueError("Display format must be either 12 or 24")

        return super().__new__(cls)

    def __init__(self, h: int, m: int, display_format: df_TimeLiteral = 24) -> None:
        Time.__last_id += 1
        self.__id = Time.__last_id
        self.h = h
        self.m = m
        self.__display_format = display_format
        self.__strdata = [
            str(h) if h > 9 else '0' + str(h),
            str(m) if m > 9 else '0' + str(m),
        ]

    def __str__(self) -> str:
        if self.__display_format == 24:
            return ":".join(self.__strdata)
        else:
            suffix = 'am' if self.h in _inclusive_range(0, 11) else 'pm'
            if self.h == 0:
                self.__strdata[0] = str(12)
            return ":".join(self.__strdata) + suffix

    def change_display_format(self, to: df_TimeLiteral) -> None:
        if to not in Time.__allowed_df_literals: raise ValueError("Display format must be either 12 or 24")

        if self.__display_format == to: return

        self.__display_format = to

class Date:
    """
    The type represents date in a format: d:m:y | m:d:y | d Month y | Month d y
    depending on display format
    """

    __slots__ = ['__id', 'd', 'm', 'y', '__strdata', '__display_format', '__month_display_format', '__year_display_format']
    __last_id = 0
    __allowed_df_literals = ['default', 'us']
    __allowed_df_month_literals = ['str', 'int']
    __allowed_df_year_literals = [2, 4]
    __current_century = 20
    __month_pairs = [
        (1, "Jan", "January"),
        (2, "Feb", "February"),
        (3, "Mar", "March"),
        (4, "Apr", "April"),
        (5, "May", "May"),
        (6, "Jun", "June"),
        (7, "Jul", "July"),
        (8, "Aug", "August"),
        (9, "Sep", "September"),
        (10, "Oct", "October"),
        (11, "Nov", "November"),
        (12, "Dec", "December")
    ]


    def __new__(cls, d: int, m: int, y: int, display_format: df_DateLiteral = 'default') -> Self:
        return super().__new__(cls)

    def __init__(self, d: int, m: int, y: int, display_format: df_DateLiteral = 'default') -> None:
        Date.__last_id += 1
        self.__id = Date.__last_id
        self.d = d
        self.m = m
        self.y = y
        self.__strdata = [
            str(d) if d > 9 else '0' + str(d),
            str(m) if m > 9 else '0' + str(m),
            str(y),
        ]
        self.__display_format: df_DateLiteral = display_format
        self.__month_display_format: df_MonthLiteral = 'int'
        self.__year_display_format: df_YearLiteral = 4

    def change_display_format(self, to: df_DateLiteral) -> None:
        if to not in Date.__allowed_df_literals: raise ValueError("Display format must be either 'default' or 'us'")

        if self.__display_format == to: return

        self.__display_format = to
        self.__strdata[0], self.__strdata[1] = self.__strdata[1], self.__strdata[0]

    def change_month_display_format(self, to: df_MonthLiteral) -> None:
        if to not in Date.__allowed_df_month_literals: raise ValueError("Month display format must be either 'str' or 'int'")

        if self.__month_display_format == to: return

        self.__month_display_format = to

        match to:
            case 'fstr':
                self.__strdata[1] = Date.__month_pairs[self.m - 1][2]
            case 'str':
                self.__strdata[1] = Date.__month_pairs[self.m - 1][1]
            case 'int':
                # notably, it would be a lil more readable if Date.__moth_pairs[self.m - 1][0] was used
                self.__strdata[1] = self.m

    def change_year_display_format(self, to: df_YearLiteral) -> None:
        if to not in Date.__allowed_df_year_literals: \
            raise ValueError("Year display format must be either 2 or 4")

        if (to == 2) and (not (Date.__current_century*100 < self.y < (Date.__current_century+1)*100)):
            raise ValueError(f"Two char length year format not allowed for this year: {self.y}")

        if self.__year_display_format == to: return

        self.__year_display_format = to

    def __str__(self) -> str:
        separator = '/' if self.__month_display_format == 'int' else ' '

        return separator.join(self.__strdata)
