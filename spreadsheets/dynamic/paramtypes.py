"""This module contains all available param types for input in a custom command
"""


__all__ = [
    'AddressParam',
    'StringParam',
    'IntegerParam',
    'FloatParam',
]


from typing import Self


from ..base.classes import Address
class AddressParam(Address):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            raise TypeError("Comparison for AddressParam must be between self and string")
        
        return f"{self.col}{self.row}" == other    

from ..libs import String, Integer, Float
from ..libs.utils import LiteralTypesExt
class ValueTypeParam:
    def __init__(self, param_type: LiteralTypesExt) -> None:
        self.param_types: list[LiteralTypesExt] = [param_type]

    def __or__(self, other: Self) -> Self:
        for param_type in other.param_types:
            if param_type in self.param_types:
                raise ValueError("Cannot assign two identical types into a combined one")

        self.param_types.extend(other.param_types)
        return self
    
    def __ror__(self, other: Self) -> Self:
        for param_type in self.param_types:
            if param_type in other.param_types:
                raise ValueError("Cannot assign two identical types into a combined one")
            
        other.param_types.extend(self.param_types)
        return self
    
StringParam = ValueTypeParam(String)
IntegerParam = ValueTypeParam(Integer)
FloatParam = ValueTypeParam(Float)