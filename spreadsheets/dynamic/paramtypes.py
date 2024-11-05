"""This module contains all available param types for input in a custom command
"""


__all__ = [
    'AddressParam',
    '_ValueTypeParam',
    'StringParam',
    'IntegerParam',
    'FloatParam',
    'ParamTypes',
]


from typing import Self
from ..libs import String


from ..base.classes import Address
from ..libs import String
class _AddressParam:
    def __str__(self) -> str:
        return 'AddressParam'

    def __eq__(self, other: object) -> bool:
        if (isinstance(other, String)) and (Address.is_valid_address_str(str(other), None)):
            return True
        
        return False
    
AddressParam = _AddressParam()

from ..libs import String, Integer, Float
from ..libs.utils import LiteralTypesExt
class _ValueTypeParam:
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
    
StringParam = _ValueTypeParam(String)
IntegerParam = _ValueTypeParam(Integer)
FloatParam = _ValueTypeParam(Float)

type ParamTypes = _AddressParam | _ValueTypeParam