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
    # 'TimePeriod',
    # 'TimeSpan',
    # 'DateSpan',
    # 'PreciseTime',
]



from enum import Enum
from typing import Literal, Self

# Df - display format
type DfTimeLiteral = Literal[12, 24]
type DfDateLiteral = Literal['default', 'us']
type DfMonthLiteral = Literal['fstr', 'str', 'int']
type DfYearLiteral = Literal[2, 4]

def _inclusive_range(start: int, stop: int) -> range:
    return range(start, stop+1)

class Time:
    """
    The type represents time in a format: H:m
    """

    __slots__ = ['__id', 'h', 'm', '__display_format', '__strdata']
    __last_id = 0
    __allowed_df_literals = [12, 24]

    def __new__(cls, h: int, m: int, display_format: DfTimeLiteral = 24) -> Self:
        if h not in _inclusive_range(0, 23):
            raise ValueError("Hour must equal any number between 0 and 23")
        if m not in _inclusive_range(0, 59):
            raise ValueError("Minute must equal any number between 0 and 59")
        if display_format not in (12, 24):
            raise ValueError("Display format must be either 12 or 24")

        return super().__new__(cls)

    def __init__(self, h: int, m: int, display_format: DfTimeLiteral = 24) -> None:
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

        suffix = 'am' if self.h in _inclusive_range(0, 11) else 'pm'

        # as in this format it is forbidden to have hour equal 0
        if self.h == 0:
            self.__strdata[0] = str(12)

        if 13 < self.h < 24:
            self.__strdata[0] = str(self.h - 12)

        return ":".join(self.__strdata) + suffix

    def change_display_format(self, to: DfTimeLiteral) -> None:
        """Changes display format of time

        Args:
            to (Literal[12, 24]):
                1) 12 - 12-hour display format with an annotation following the time
                (12:44 am, 7:23 am, 9:37 pm, 12:33 pm)
                2) 24 - 24-hour display format. Plain hour and minutes
                (12:44, 19:23, 21:37, 0:33)
        """
        if to not in Time.__allowed_df_literals:
            raise ValueError("Display format must be either 12 or 24")

        if self.__display_format == to:
            return

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
    __months = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ]


    def __new__(cls, d: int, m: int, y: int, display_format: DfDateLiteral = 'default') -> Self:
        return super().__new__(cls)

    def __init__(self, d: int, m: int, y: int, display_format: DfDateLiteral = 'default') -> None:
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
        self.__display_format: DfDateLiteral = display_format
        self.__month_display_format: DfMonthLiteral = 'int'
        self.__year_display_format: DfYearLiteral = 4

    def change_display_format(self, to: DfDateLiteral) -> None:
        """Changes display format of date

        Args:
            to (Literal['default', 'us']):
                1) 'default': displays day first, then month
                (24/07/2024, 24 July 2024, 24/07/24, 24 Jul 2024)
                2) 'us': us display format, where month is displayed first, then day
                (07/24/2024, July 24 2024, 07/24/24, Jul 24 2024)
        """
        if to not in Date.__allowed_df_literals:
            raise ValueError("Display format must be either 'default' or 'us'")

        if self.__display_format == to:
            return

        self.__display_format = to
        self.__strdata[0], self.__strdata[1] = self.__strdata[1], self.__strdata[0]

    def change_month_display_format(self, to: DfMonthLiteral, *, auto: bool = False) -> None:
        """Changes month display format

        Args:
            to (DfMonthLiteral): 
                1) 'fstr': displays month as a word. Will be shown all letters in the month's name 
                (February, October)
                Note: cannot set to this display format if year format is 2 char long.
                2) 'str': displays month as a three character long word.
                (Feb, Oct)
                Note: cannot set to this display format if year format is 2 char long.
                3) 'int': displays month as a number, according to its order
                
            auto (bool, optional): 
                changes automatically year display format if contradiction occurs. 
                Not recommended to use. Defaults to False.

        """
        if to not in Date.__allowed_df_month_literals:
            raise ValueError("Month display format must be either 'str' or 'int'")

        if (to != 'int') and (self.__year_display_format == 2):
            if not auto:
                raise ValueError(f"Can't set month display format to {to} as year display format is 2 char long")

            self.__year_display_format = 4

        if self.__month_display_format == to:
            return

        self.__month_display_format = to

        match to:
            case 'fstr':
                self.__strdata[1] = Date.__months[self.m - 1]
            case 'str':
                self.__strdata[1] = Date.__months[self.m - 1][0:3]
            case 'int':
                self.__strdata[1] = self.m

    def change_year_display_format(self, to: DfYearLiteral, *, auto: bool = False) -> None:
        """Changes month display format

        Args:
            to (DfMonthLiteral): 
                1) 2: two characters long year display. 
                Allowed for years that are in current century. 
                Not allowed for the year that ends on 00
                (For 20th century: 01, 09, 11, 16, 24, 25, 26, 27)
                2) 4: four characters long year display. 
                Also works for any year that is not four-char-long
                (2001, 1999, 1456, 2568)
                
            auto (bool, optional): 
                changes automatically month display format if contradiction occurs. 
                Not recommended to use. Defaults to False.

        """
        if to not in Date.__allowed_df_year_literals:
            raise ValueError("Year display format must be either 2 or 4")

        if to == 2:
            if not Date.__current_century*100 < self.y < (Date.__current_century+1)*100:
                raise ValueError(f"Two char length year format not allowed for this year: {self.y}")

            if self.__month_display_format != 'int':
                if not auto:
                    raise ValueError(f"Can't set year display format, as month display format is {self.__month_display_format}")

                self.__month_display_format = 'int'

        if self.__year_display_format == to:
            return

        self.__year_display_format = to

    def __str__(self) -> str:
        separator = '/' if self.__month_display_format == 'int' else ' '

        return separator.join(self.__strdata)
