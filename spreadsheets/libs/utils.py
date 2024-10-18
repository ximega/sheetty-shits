__all__ = [
    '_LiteralTypes',
]



from .string import String
from .integer import Integer


type _LiteralTypes = type[String] | type[Integer]