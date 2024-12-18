"""
This library is a extension to libs.time and contains following time types:
TimePeriod (i.e. 5 minutes, 5 m)
DatePeriod (i.e. 5 days)
DateTimePeriod (DatePeriod and TimePeriod combination)
TimeSpan (i.e. 14:55-15:03)
DateSpan (i.e. 04/06/2024-30/06/2024)
DateTimeSpan (DateSpan and TimeSpan combination)
"""


__all__ = [
    'TimePeriod',
    'DatePeriod',
    'DateTimePeriod',
    'TimeSpan',
    'DateSpan',
    'DateTimeSpan',
]



from typing import Self
from datetime import datetime

from .time import Time, Date, PreciseTime, DateTime
from . import Null


type PositiveNumber = int
type CustomTime = str
type TimeFormat = str


class TimePeriod:
    """
    This type represents any period of time.
    Theoretically it is a just a time given,
    but updates time until it reaches 0, when it will be replaced with libs.Null
    """

    def __new__(cls, time: Time | PreciseTime) -> Self:
        return super().__new__(cls)

    def __init__(self, time: Time | PreciseTime) -> None:
        self.h = time.h
        self.m = time.m
        if isinstance(time, PreciseTime):
            self.s = time.s
            self.ms = time.ms

        self.__strdata: list[str] = [
            str(self.h),
            str(self.m) if self.m > 9 else '0' + str(self.m)
        ]
        if self.s is not None:
            self.__strdata.append(str(self.s) if self.s > 9 else '0' + str(self.s))
        if self.ms is not None:
            self.__strdata.append(str(self.ms) if self.ms > 9 else '0' + str(self.ms))

    def update(self) -> None:
        """Updates the value of self, decreasing it, until it reaches 0 and turns into NULL
        """
        now = datetime.today()
        then: datetime | None = None
        if (self.ms is None) or (self.s is None):
            then = datetime(now.year, now.month, now.day, hour=self.h, minute=self.m)
        else:
            then = datetime(now.year, now.month, now.day, hour=self.h, minute=self.m, second=self.s, microsecond=self.ms)

        diff = now - then
        new = then - diff

        self.h: int = new.hour
        self.m: int = new.minute
        self.s: int | None = new.second if new.second != 0 else None
        self.ms: int | None = new.microsecond if new.microsecond != 0 else None

        self.__strdata = [
            str(self.h),
            str(self.m) if self.m > 9 else '0' + str(self.m)
        ]
        if self.s is not None:
            self.__strdata.append(str(self.s) if self.s > 9 else '0' + str(self.s))
        if self.ms is not None:
            self.__strdata.append(str(self.ms) if self.ms > 9 else '0' + str(self.ms))

class DatePeriod:
    """_summary_
    """

class DateTimePeriod:
    """_summary_
    """

class TimeSpan:
    """_summary_
    """

class DateSpan:
    """_summary_
    """

class DateTimeSpan:
    """_summary_
    """