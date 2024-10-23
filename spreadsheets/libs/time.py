"""
This library contains necessary time-related types, like:
Time (i.e. 14:43)
Date (i.e. 07/12/2024)
DateTime (i.e. 04/06/2024 14:55)
PreciseTime (i.e. 06:15:22, 22:04:24:453)
"""


__all__ = [
    'Time',
    'Date',
    'PreciseTime',
    'DateTime',
]



from typing import Self
from enum import Enum, auto

type PositiveNumber = int


def _inclusive_range(start: int, stop: int) -> range:
    return range(start, stop+1)


class DfTime(Enum):
    H24 = auto()
    H12 = auto()
    FSTR = auto()
    STR = auto()

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

    def __new__(cls,
                h: PositiveNumber, m: PositiveNumber,
                display_format: DfTime = DfTime.H24
        ) -> Self:

        if not 0 <= h <= 23:
            raise ValueError("Hour must equal any number between 0 and 23")
        if not 0 <= m <= 59:
            raise ValueError("Minute must equal any number between 0 and 59")

        if display_format not in DfTime:
            raise ValueError("Display format must be from DfTime")

        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self, h: PositiveNumber, m: PositiveNumber, display_format: DfTime = DfTime.H24) -> None:
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
            case DfTime.H24:
                return ":".join(self.__strdata)
            case DfTime.H12:
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
            case DfTime.FSTR:
                return f"{self.h} hour{'s' if self.h != 1 else ''} \
                         and {self.m} minute{'s' if self.m != 1 else ''}"
            case DfTime.STR:
                return f"{self.h} h {self.m} m"

    def __repr__(self) -> str:
        return f"<Time> id: {self.__id} \
            \nvalue: {self.__str__()}"

    def change_display_format(self, to: DfTime) -> None:
        """Changes display format of time

        Args:
            to (DfTime):
                1) DfTime.H12 - 12-hour display format with an annotation following the time
                (12:44 am, 7:23 am, 9:37 pm, 12:33 pm)
                2) DfTime.H24 - 24-hour display format. Plain hour and minutes
                (12:44, 19:23, 21:37, 0:33)
                3) DfTime.FSTR - displays words 'hours' and 'minutes' as full words
                4) DfTime.STR - displays words 'hours' and 'minutes'
                as shortened words with first letter
        """
        if to not in DfTime:
            raise ValueError("Display format must be from DfTime")

        if self.__display_format == to:
            return

        self.__display_format = to

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
    __current_century = 20
    __months = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ]


    @classmethod
    def is_leap_year(cls, year: PositiveNumber) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def __new__(cls,
            d: PositiveNumber, m: PositiveNumber, y: PositiveNumber,
            display_format: DfDate = DfDate.DEFAULT
        ) -> Self:

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

        if display_format not in DfDate:
            raise ValueError("display_format must be from DfDate")

        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self,
            d: PositiveNumber, m: PositiveNumber, y: PositiveNumber,
            display_format: DfDate = DfDate.DEFAULT
        ) -> None:

        self.__id = self.__last_id
        self.d = d
        self.m = m
        self.y = y
        self.__strdata = [
            str(d) if d > 9 else '0' + str(d),
            str(m) if m > 9 else '0' + str(m),
            str(y),
        ]
        self.__display_format: DfDate = display_format
        self.__month_display_format: DfDateMonth = DfDateMonth.INT
        self.__year_display_format: DfDateYear = DfDateYear.CHAR4

    def change_display_format(self, to: DfDate) -> None:
        """Changes display format of date

        Args:
            to (DfDate):
                1) DfDate.DEFAULT: displays day first, then month
                (24/07/2024, 24 July 2024, 24/07/24, 24 Jul 2024)
                2) DfDate.EN_US: us display format, where month is displayed first, then day
                (07/24/2024, July 24 2024, 07/24/24, Jul 24 2024)
        """
        if to not in DfDate:
            raise ValueError("Display format must be either 'default' or 'en-us'")

        if self.__display_format == to:
            return

        self.__display_format = to
        self.__strdata[0], self.__strdata[1] = self.__strdata[1], self.__strdata[0]

    def change_month_display_format(self, to: DfDateMonth, *, auto_force: bool = False) -> None:
        """Changes month display format

        Args:
            to (DfMonthLiteral):
                1) DfDateMonth.FSTR: displays month as a word.
                Will be shown all letters in the month's name
                (February, October)
                Note: cannot set to this display format if year format is 2 char long.
                2) DfDateMonth.STR: displays month as a three character long word.
                (Feb, Oct)
                Note: cannot set to this display format if year format is 2 char long.
                3) DfDateMonth.INT: displays month as a number, according to its order

            auto_force (bool, optional):
                changes automatically year display format if contradiction occurs.
                Not recommended to use. Defaults to False.

        """
        if to not in DfDateMonth:
            raise ValueError("Month display format must be from DfDateMonth")

        if (to != DfDateMonth.INT) and (self.__year_display_format == DfDateYear.CHAR2):
            if not auto_force:
                raise ValueError(f"Can't set month display format to {to} as year display format is 2 char long")

            self.__year_display_format = DfDateYear.CHAR4
            self.__strdata[2] = str(self.y)

        if self.__month_display_format == to:
            return

        self.__month_display_format = to

        match to:
            case DfDateMonth.FSTR:
                self.__strdata[1] = self.__months[self.m - 1]
            case DfDateMonth.STR:
                self.__strdata[1] = self.__months[self.m - 1][0:3]
            case DfDateMonth.INT:
                self.__strdata[1] = str(self.m) if self.m > 9 else '0' + str(self.m)

    def change_year_display_format(self, to: DfDateYear, *, auto_force: bool = False) -> None:
        """Changes month display format

        Args:
            to (DfDateYear):
                1) DfDateYear.CHAR2: two characters long year display.
                Allowed for years that are in current century.
                Not allowed for the year that ends on 00
                (For 20th century: 01, 09, 11, 16, 24, 25, 26, 27)
                2) DfDateYear.CHAR4: four characters long year display.
                Also works for any year that is not four-char-long
                (2001, 1999, 1456, 2568)

            auto_force (bool, optional):
                changes automatically month display format if contradiction occurs.
                Not recommended to use. Defaults to False.

        """
        if to not in DfDateYear:
            raise ValueError("Year display format must be either 2 or 4")

        if to == DfDateYear.CHAR2:
            if not self.__current_century*100 < self.y < (self.__current_century+1)*100:
                raise ValueError(f"Two char length year format not allowed for this year: {self.y}")

            if self.__month_display_format != DfDateMonth.INT:
                if not auto_force:
                    raise ValueError(f"Can't set year display format, as month display format is {self.__month_display_format}")

                self.__month_display_format = DfDateMonth.INT

        if self.__year_display_format == to:
            return

        self.__year_display_format = to

        match to:
            case DfDateYear.CHAR2:
                self.__strdata[2] = str(self.y)[2:]
            case DfDateYear.CHAR4:
                self.__strdata[2] = str(self.y)

    def __str__(self) -> str:
        separator = '/' if self.__month_display_format == DfDateMonth.INT else ' '

        return separator.join(self.__strdata)

    def __repr__(self) -> str:
        return f"<Date> id: {self.__id} \
                 \nvalue: {self.__str__()}"

class DfPreciseTime(Enum):
    FSTR = auto()
    STR = auto()
    INT = auto()

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

    def __new__(cls,
            h: PositiveNumber, m: PositiveNumber, s: PositiveNumber, ms: PositiveNumber | None = None,
            display_format: DfPreciseTime = DfPreciseTime.FSTR
        ) -> Self:

        if not 1 <= h <= 23:
            raise ValueError("Hour must equal any number between 1 and 23")
        if not 0 <= m <= 59:
            raise ValueError("Minute must equal any number between 0 and 59")
        if not 0 <= s <= 59:
            raise ValueError("Second must equal any number between 0 and 59")
        if ms is not None:
            if not 0 <= ms <= 999:
                raise ValueError("Millisecond must equal any number between 0 and 59")

        if display_format not in DfPreciseTime:
            raise ValueError("Display format must be from DfPreciseTime")

        return super().__new__(cls)

    def __init__(self,
            h: PositiveNumber, m: PositiveNumber, s: PositiveNumber, ms: PositiveNumber | None = None,
            display_format: DfPreciseTime = DfPreciseTime.FSTR
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

    def change_display_format(self, to: DfPreciseTime):
        """Changes display format of PreciseTime

        Args:
            to (DfPreciseTime):
                1) DfPreciseTime.FSTR: will display units with their integer value
                2) DfPreciseTime.STR: will display shortened versions of units (1 char)
                with their integer value
        """

        if to not in DfPreciseTime:
            raise ValueError("Display format must from DfPreciseTime")

        if to == self.__display_format:
            return

        self.__display_format = to

    def __str__(self) -> str:
        if self.__display_format == DfPreciseTime.INT:
            return ":".join(self.__strdata)

        unit_words = [('hour', 'h'), ('minute', 'm'), ('second', 's'), ('millisecond', 'ms')]
        ret: list[str] = []

        for index, unit in enumerate(self.__strdata):
            if int(unit) == 0:
                continue

            unit_word = unit_words[index][0] if self.__display_format == DfPreciseTime.FSTR else unit_words[index][1]
            suffix = 's' if int(unit) > 1 else ''
            ret.append(f"{unit} {unit_word}{suffix if self.__display_format == DfPreciseTime.FSTR else ''}")

        return " ".join(ret)

    def __repr__(self) -> str:
        return f"<Time> id: {self.__id} \
                 \nvalue: {self.__str__()}"


class DfDateTime(Enum):
    FSTR = auto()
    STR = auto()
    INT = auto()
    FULL_STR = auto()

class RegDateTime(Enum):
    DEFAULT = auto()
    US = auto()

class DateTime:
    """Combine two time types: time.Time and time.Date
    """

    __slots__ = [
        '__id',
        'd', 'm', 'y', 'h', 'mn', 's', 'ms',
        '__strdata',
        '__display_format', '__region_format'
    ]
    __last_id = 0
    __current_century = 20
    __months = [
        "January", "February", "March",
        "April", "May", "June",
        "July", "August", "September",
        "October", "November", "December"
    ]
    __unit_words = [
        ('day', 'd'), ('month', 'm'), ('year', 'y'),
        ('hour', 'h'), ('minute', 'mn'), ('second', 's'), ('millisecond', 'ms')
    ]


    @classmethod
    def is_leap_year(cls, year: PositiveNumber) -> bool:
        """Determines whether given year is a leap or not
        """
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def __new__(cls,
            d: PositiveNumber, m: PositiveNumber, y: PositiveNumber,
            h: PositiveNumber, mn: PositiveNumber, s: PositiveNumber, ms: PositiveNumber | None = None,
            display_format: DfDateTime = DfDateTime.INT, region_format: RegDateTime = RegDateTime.DEFAULT
        ) -> Self:

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

        if display_format not in DfDateTime:
            raise ValueError("Date display format must be from DfDate")

        if not 0 <= h <= 23:
            raise ValueError("Hour must equal any number between 0 and 23")
        if not 0 <= mn <= 59:
            raise ValueError("Minute must equal any number between 0 and 59")
        if not 0 <= s <= 59:
            raise ValueError("Second must equal any number between 0 and 59")
        if (ms is not None) and (not 0 <= ms <= 999):
            raise ValueError("Millisecond must equal any number between 1 and 999")

        cls.__last_id += 1
        return super().__new__(cls)

    def __init__(self,
            d: PositiveNumber, m: PositiveNumber, y: PositiveNumber,
            h: PositiveNumber, mn: PositiveNumber, s: PositiveNumber, ms: PositiveNumber | None = None,
            display_format: DfDateTime = DfDateTime.INT, region_format: RegDateTime = RegDateTime.DEFAULT
        ) -> None:

        self.__id = self.__last_id
        self.d = d
        self.m = m
        self.y = y
        self.h = h
        self.mn = mn
        self.s = s
        self.ms = ms
        self.__strdata = [
            str(d) if d > 9 else '0' + str(d),
            str(m) if m > 9 else '0' + str(m),
            str(y),
            str(h) if h > 9 else '0' + str(h),
            str(mn) if mn > 9 else '0' + str(mn),
            str(s) if s > 9 else '0' + str(s),
        ]
        if ms is not None:
            self.__strdata.append('0'*(3-len(str(ms))) + str(ms))
        self.__display_format: DfDateTime = display_format
        self.__region_format: RegDateTime = region_format

    def __str__(self) -> str:
        date_separator = '/' if self.__display_format == DfDateTime.INT else ' '
        time_separator = ':' if self.__display_format == DfDateTime.INT else ' '

        return date_separator.join(self.__strdata[0:3]) + ' ' + time_separator.join(self.__strdata[3:])

    def __repr__(self) -> str:
        return f"<DateTime> id: {self.__id} \
                 \nvalue: {self.__str__()}"

    def change_display_format(self, to: DfDateTime) -> None:
        """Changes display format of DateTime

        Args:
            to (DfDateTime):
                1) DfDateTime.FSTR: will display month as word, thus changing formatting
                2) DfDateTime.STR: will display shortened version of month
                3) DfDateTime.INT: will display month as a int
                4) DfDateTime.FULL_STR: will display all units as words.
        """
        if to not in DfDateTime:
            raise ValueError("Display format must be form DfDateTime")

        if to == self.__display_format:
            return

        month_index: int = 1 if self.__region_format == RegDateTime.DEFAULT else 0

        self.__display_format = to

        match to:
            case DfDateTime.FSTR:
                for index, strdata in enumerate(self.__strdata):
                    value: int = getattr(self, self.__unit_words[index][1])
                    self.__strdata[index] = str(value) if value > 9 else '0' + str(value)
                self.__strdata[month_index] = self.__months[self.m - 1]
            case DfDateTime.STR:
                for index, strdata in enumerate(self.__strdata):
                    value: int = getattr(self, self.__unit_words[index][1])
                    self.__strdata[index] = str(value) if value > 9 else '0' + str(value)
                self.__strdata[month_index] = self.__months[self.m - 1][0:3]
            case DfDateTime.INT:
                for index, strdata in enumerate(self.__strdata):
                    value: int = getattr(self, self.__unit_words[index][1])
                    self.__strdata[index] = str(value) if value > 9 else '0' + str(value)
            case DfDateTime.FULL_STR:
                for index, strdata in enumerate(self.__strdata):
                    self.__strdata[index] = str(int(strdata)) + ' ' + self.__unit_words[index][0]
                    self.__strdata[index] += 's' if int(strdata) > 0 else ''

    def change_region_format(self, to: RegDateTime) -> None:
        """Changes region format.

        Args:
            to (RegDateTime):
                1) RegDateTime.DEFAULT: day shown first, month second
                2) RegDateTime.US: month shown first, date shown second
        """
        if to not in RegDateTime:
            raise ValueError("Region format must be from RegDateTime")

        if to == self.__region_format:
            return

        self.__region_format = to
        self.__strdata[0], self.__strdata[1] = self.__strdata[1], self.__strdata[0]
        self.__unit_words[0], self.__unit_words[1] = self.__unit_words[1], self.__unit_words[0]
