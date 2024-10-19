__all__ = [
    '_LiteralTypes',
    '_highest_power_of'
]



from .string import String
from .integer import Integer


type _LiteralTypes = type[String] | type[Integer]


def _highest_power_of(number: int, base: int) -> int:
    power = 0
    while base ** (power + 1) <= number:
        power += 1
    return power