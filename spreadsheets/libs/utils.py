__all__ = [
    'LiteralTypes',
    'highest_power_of',
    'LiteralTypesExt',
    'CellValues'
]



from .string import String
from .integer import Integer
from .float import Float
from .array import Array
from .multiple import Multiple
from .time import Time, Date, PreciseTime, DateTime
from .period import TimePeriod


type LiteralTypes = type[String] | type[Integer] | type[Float] | type[Array]
type LiteralTypesExt = LiteralTypes | type[Multiple] \
                       | type[Time] | type[Date] | type[PreciseTime] | type[DateTime] \
                       | type[TimePeriod]
type CellValues = String | Integer | Float | Array | Multiple \
                  | Time | Date | PreciseTime | DateTime \
                  | TimePeriod


def highest_power_of(number: int, base: int) -> int: # type: ignore
    power = 0
    while base ** (power + 1) <= number:
        power += 1
    return power

type CustomTime = str
type TimeFormat = str

type TimeTypes = Time | Date | PreciseTime | DateTime | TimePeriod
type TimeLiteralTypes = type[Time] | type[Date] | type[PreciseTime] | type[DateTime] | type[TimePeriod]

def extract_time(time: CustomTime, format: TimeFormat, type_to: TimeLiteralTypes) -> TimeTypes:
    ...