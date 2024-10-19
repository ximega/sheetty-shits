__all__ = [
    '_LiteralTypes',
    '_highest_power_of',
    '_LiteralTypesExt',
    '_CellValues'
]



from .string import String
from .integer import Integer
from .array import Array
from .multiple import Multiple


type _LiteralTypes = type[String] | type[Integer] | type[Array]
type _LiteralTypesExt = _LiteralTypes | type[Multiple]
type _CellValues = String | Integer | Array | Multiple


def _highest_power_of(number: int, base: int) -> int:
    power = 0
    while base ** (power + 1) <= number:
        power += 1
    return power