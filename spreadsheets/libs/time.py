"""
This library contains necessary time-related types, like:
Time (i.e. 14:43)
Date (i.e. 07/12/2024)
PreciseTime (i.e. 06:15:22, 22:04:24:453)
CombinedTime (i.e. 04/06/2024 14:55)
TimePeriod (i.e. 5 minutes, 5 m)
DatePeriod (i.e. 5 days)
TimeSpan (i.e. 14:55-15:03)
DateSpan (i.e. 04/06/2024-30/06/2024)
"""


__all__ = [
    'Time',
    'Date',
    'PreciseTime',
    'DateTime',
    'TimePeriod',
    # 'DatePeriod'
    # 'TimeSpan',
    # 'DateSpan',
]



from enum import Enum
from typing import Literal, Self

type PositiveNumber = int
# Df - display format
type DfTimeLiteral = Literal[12, 24, 'fstr', 'str']
type DfDateLiteral = Literal['default', 'en-us']
type DfMonthLiteral = Literal['fstr', 'str', 'int']
type DfYearLiteral = Literal[2, 4]
type DfPreciseTimeLiteral = Literal['fstr', 'str']
type CustomTime = str
type TimeFormat = str

def _inclusive_range(start: int, stop: int) -> range:
    return range(start, stop+1)



class Time:
    """
    The type represents time in a format: H:m
    """

    __slots__ = [
        '__id',
        'h', 'm',
        '__display_format',
        '__strdata'
    ]
    __last_id = 0
    __allowed_df_literals = [12, 24, 'fstr', 'str']

    def __new__(cls, h: PositiveNumber, m: PositiveNumber, display_format: DfTimeLiteral = 24) -> Self:
        if not 0 <= h <= 23:
            raise ValueError("Hour must equal any number between 0 and 23")
        if not 0 <= m <= 59:
            raise ValueError("Minute must equal any number between 0 and 59")
        if display_format not in cls.__allowed_df_literals:
            raise ValueError("Display format must be either 12, 24 or 'str'")

        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, h: PositiveNumber, m: PositiveNumber, display_format: DfTimeLiteral = 24) -> None:
        self.__id = self.__last_id
        self.h = h
        self.m = m
        self.__display_format = display_format
        self.__strdata = [
            str(h) if h > 9 else '0' + str(h),
            str(m) if m > 9 else '0' + str(m),
        ]

    def __str__(self) -> str:
        match self.__display_format:
            case 24:
                return ":".join(self.__strdata)
            case 12:
                suffix = ' am' if self.h in _inclusive_range(0, 11) else ' pm'

                # as in this format it is forbidden to have hour equal 0
                if self.h == 0:
                    self.__strdata[0] = str(12)

                if 13 < self.h < 24:
                    self.__strdata[0] = str(self.h - 12)

                if 0 < int(self.__strdata[0]) < 9:
                    self.__strdata[0] = '0' + self.__strdata[0][-1]

                if 0 < int(self.__strdata[1]) < 9:
                    self.__strdata[1] = '0' + self.__strdata[1][-1]

                return ":".join(self.__strdata) + suffix
            case 'fstr':
                return f"{self.h} hour{'s' if self.h != 1 else ''} and {self.m} minute{'s' if self.m != 1 else ''}"
            case 'str':
                return f"{self.h} h {self.m} m"

    def __repr__(self) -> str:
        return f"<Time> id: {self.__id} \
            \nvalue: {self.__str__()}"

    def change_display_format(self, to: DfTimeLiteral) -> None:
        """Changes display format of time

        Args:
            to (Literal[12, 24, 'fstr', 'str']):
                1) 12 - 12-hour display format with an annotation following the time
                (12:44 am, 7:23 am, 9:37 pm, 12:33 pm)
                2) 24 - 24-hour display format. Plain hour and minutes
                (12:44, 19:23, 21:37, 0:33)
                3) 'fstr' - displays words 'hours' and 'minutes' as full words
                4) 'str' - displays words 'hours' and 'minutes' as shortened words with first letter
        """
        if to not in self.__allowed_df_literals:
            raise ValueError("Display format must be either 12, 24, 'fstr' or 'str'")

        if self.__display_format == to:
            return

        self.__display_format = to

class Date:
    """
    The type represents date in a format: d:m:y | m:d:y | d Month y | Month d y
    depending on display format
    """

    __slots__ = [
        '__id',
        'd', 'm', 'y',
        '__strdata',
        '__display_format', '__month_display_format', '__year_display_format'
    ]
    __last_id = 0
    __allowed_df_literals = ['default', 'en-us']
    __allowed_df_month_literals = ['fstr', 'str', 'int']
    __allowed_df_year_literals = [2, 4]
    __current_century = 20
    __months = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ]


    @classmethod
    def is_leap_year(cls, year) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def __new__(cls, d: PositiveNumber, m: PositiveNumber, y: PositiveNumber, display_format: DfDateLiteral = 'default') -> Self:
        if not 1 <= d <= 31:
            raise ValueError("The day must be between 1 and 31")

        if not 1 <= m <= 12:
            raise ValueError("The month must be between 1 and 12")

        # February
        if m == 2:
            if cls.is_leap_year(y) and d > 29:
                raise ValueError("The day cannot be more than 29 in leap-year February")

            if d > 28:
                raise ValueError("The day cannot be more than 28 in February")

        # April, June, September, November
        if (m in [4, 6, 9, 11]) and (d > 30):
            raise ValueError(f"The day cannot be more than 30 in {cls.__months[m-1]}")

        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, d: PositiveNumber, m: PositiveNumber, y: PositiveNumber, display_format: DfDateLiteral = 'default') -> None:
        self.__id = self.__last_id
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
            to (Literal['default', 'en-us']):
                1) 'default': displays day first, then month
                (24/07/2024, 24 July 2024, 24/07/24, 24 Jul 2024)
                2) 'en-us': us display format, where month is displayed first, then day
                (07/24/2024, July 24 2024, 07/24/24, Jul 24 2024)
        """
        if to not in self.__allowed_df_literals:
            raise ValueError("Display format must be either 'default' or 'en-us'")

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
        if to not in self.__allowed_df_month_literals:
            raise ValueError("Month display format must be either 'str' or 'int'")

        if (to != 'int') and (self.__year_display_format == 2):
            if not auto:
                raise ValueError(f"Can't set month display format to {to} as year display format is 2 char long")

            self.__year_display_format = 4
            self.__strdata[2] = str(self.y)

        if self.__month_display_format == to:
            return

        self.__month_display_format = to

        match to:
            case 'fstr':
                self.__strdata[1] = self.__months[self.m - 1]
            case 'str':
                self.__strdata[1] = self.__months[self.m - 1][0:3]
            case 'int':
                self.__strdata[1] = str(self.m) if self.m > 9 else '0' + str(self.m)

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
        if to not in self.__allowed_df_year_literals:
            raise ValueError("Year display format must be either 2 or 4")

        if to == 2:
            if not self.__current_century*100 < self.y < (self.__current_century+1)*100:
                raise ValueError(f"Two char length year format not allowed for this year: {self.y}")

            if self.__month_display_format != 'int':
                if not auto:
                    raise ValueError(f"Can't set year display format, as month display format is {self.__month_display_format}")

                self.__month_display_format = 'int'

        if self.__year_display_format == to:
            return

        self.__year_display_format = to

        match to:
            case 2:
                self.__strdata[2] = str(self.y)[2:]
            case 4:
                self.__strdata[2] = str(self.y)

    def __str__(self) -> str:
        separator = '/' if self.__month_display_format == 'int' else ' '

        return separator.join(self.__strdata)

    def __repr__(self) -> str:
        return f"<Date> id: {self.__id} \
            \nvalue: {self.__str__()}"

class PreciseTime:
    """An expansion to libs.time.Time type

    Allows to add seconds and milliseconds to time
    """

    __slots__ = [
        '__id',
        'h', 'm', 's', 'ms',
        '__display_format',
        '__strdata'
    ]
    __last_id = 0
    __allowed_df_literals = ['fstr', 'str']

    def __new__(cls,
            h: PositiveNumber, m: PositiveNumber, s: PositiveNumber, ms: PositiveNumber = None,
            display_format: DfTimeLiteral = 'fstr'
        ) -> Self:

        if not 1 <= h <= 23:
            raise ValueError("Hour must equal any number between 1 and 23")
        if not 0 <= m <= 59:
            raise ValueError("Minute must equal any number between 0 and 59")
        if not 0 <= s <= 59:
            raise ValueError("Second must equal any number between 0 and 59")
        if not 0 <= ms <= 999:
            raise ValueError("Millisecond must equal any number between 0 and 59")

        if display_format not in cls.__allowed_df_literals:
            raise ValueError(f"Display format must equal one of following: {",".join(cls.__allowed_df_literals)}")

        return super().__new__(cls)

    def __init__(self,
            h: PositiveNumber, m: PositiveNumber, s: PositiveNumber, ms: PositiveNumber = None,
            display_format: DfPreciseTimeLiteral = 'fstr'
        ) -> None:

        self.__id = self.__last_id
        self.h = h
        self.m = m
        self.s = s
        self.ms = ms
        self.__display_format = display_format
        self.__strdata = [
            str(h),
            str(m) if m > 9 else '0' + str(m),
            str(s) if s > 9 else '0' + str(s),
        ]
        if ms is not None:
            self.__strdata.append(str(ms) if ms > 9 else '0' + str(ms))

    def change_display_format(self, to: DfPreciseTimeLiteral):
        """Changes display format of PreciseTime

        Args:
            to (DfPreciseTimeLiteral): 
                1) 'fstr': will display units with their integer value
                2) 'str': will display shortened versions of units (1 char) with their integer value
        """

        if to not in self.__allowed_df_literals:
            raise ValueError(f"Display format must equal one of following: {",".join(self.__allowed_df_literals)}")

        if to == self.__display_format:
            return

        self.__display_format = to

    def __str__(self) -> str:
        unit_words = [('hour', 'h'), ('minute', 'm'), ('second', 's'), ('millisecond', 'ms')]
        ret: list[str] = []

        for index, unit in enumerate(self.__strdata):
            if int(unit) == 0:
                continue

            unit_word = unit_words[index][0] if self.__display_format == 'fstr' else unit_words[index][1]
            suffix = 's' if int(unit) > 1 else ''
            ret.append(f"{unit} {unit_word}{suffix if self.__display_format == 'fstr' else ''}")

        return " ".join(ret)

    def __repr__(self) -> str:
        return f"<Time> id: {self.__id} \
            \nvalue: {self.__str__()}"

class DateTime:
    pass

class TimePeriod:
    """
    This type represents any period of time.
    Theoretically it is a just a time given,
    but updates time until it reaches 0, when it will be replaced with libs.Null
    """

    def __new__(cls) -> Self:
        pass

    def __init__(self, time: Time | PreciseTime | DateTime) -> None:
        pass


type TimeTypes = Time | Date | PreciseTime | DateTime | TimePeriod
type TimeLiteralTypes = type[Time] | type[Date] | type[PreciseTime] | type[DateTime] | type[TimePeriod]

def extract_time(time: CustomTime, format: TimeFormat, type_to: TimeLiteralTypes) -> TimeTypes:
    return