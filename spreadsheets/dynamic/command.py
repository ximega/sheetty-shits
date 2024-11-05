"""
This module allows a user to create and manage custom command in a dynamic mode.
"""


__all__ = [
    'Console'
]



from typing import Any
from collections.abc import Callable
from .paramtypes import *
from ..libs import Integer, Float, String, boolTrue, boolFalse


class _CustomCommand:
    def __init__(self,
            name: str,
            argc: set[str],
            argv: set[str],
            param_types: list[ParamTypes],
            docs: str,
            handler: Callable[[Any, set[str], set[str], list[Any]], Any],
        ) -> None:
        
        self.name: str = name
        self.argc: set[str] = argc
        self.argv: set[str] = argv
        self.param_types: list[ParamTypes] = param_types 
        self.docs: str = docs
        self.handler = handler

    def call(self, sp: Any, argc: set[str], argv: set[str], params: list[str]) -> str:
        # again, Any is specified as a type of sp
        # not to cause circular import error
        """Calls a command"""
        val_argc: set[str] = argc - self.argc
        if len(val_argc) > 0:
            raise ValueError(f"Unknown value of 'argc': {val_argc}")
        val_argv: set[str] = argv - self.argv
        if len(val_argv) > 0:
            raise ValueError(f"Unknown value of 'argv': {val_argv}")
        
        for index, param in enumerate(params):
            param_type: ParamTypes = self.param_types[index]

            if param.isdigit():
                param = Integer(int(param))
            else:
                try:
                    param = Float(float(param))
                except ValueError:
                    match param:
                        case 'TRUE':
                            param = boolTrue
                        case 'FALSE':
                            param = boolFalse
                        case _:
                            param = String(param)
   
            allow_access: bool = False

            if param == AddressParam:
                allow_access = True
            if isinstance(param_type, _ValueTypeParam):
                for param_type_singular in param_type.param_types:
                    if isinstance(param, param_type_singular):
            # NOTE: 
            # add more handlers for checking types in the future 
            # if any created in paramtypes.py

            if not allow_access:
                raise ValueError(f"The value of {param} is not associated with type it was given in param_types ({param_type})")
            
            return self.handler()
 
class Console:
    """The class allows manipulations with a dynamic console
    str() and repr() are not allowed to be called on this class
    The inputs during initialization must be of type Spreadsheets. 
    Not provided literally as a type since it will cause circular import
    """
    __slots__ = ['__sp', '__commands']

    def __init__(self, sp: Any) -> None:
        self.__sp: Any = sp
        self.__commands: dict[str, _CustomCommand] = {}

    def __str__(self) -> str:
        raise ReferenceError("Cannot use str() over Console")
    
    def __repr__(self) -> str:
        raise ReferenceError("Cannot use repr() over Console")

    def add_handler(self, 
            name: str, 
            argc: set[str], argv: set[str], 
            param_types: list[ParamTypes], 
            docs: str, 
            # the first Any is actually Spreadsheets, 
            # but trying to import it and specify as a type 
            # would cause Circular Import Error
            # the second is argc, third argv, the fourth are the params
            # the ReturnType is str, as a custom command must always return some response to be printed out
            # NOTE: this must be added to a docs btw
            handler: Callable[[Any, set[str], set[str], list[ParamTypes]], str]
        ) -> _CustomCommand: 

        """Adds a custom command"""
        command = _CustomCommand(name, argc, argv, param_types, docs, handler)

        self.__commands[name] = command
        return command
    
    def all_commands(self) -> dict[str, _CustomCommand]:
        """Lists all commands"""
        return self.__commands
    
    def call(self, name: str, **kwargs: set[str] | list[str]) -> str:
        if not isinstance(kwargs['argc'], set):
            raise TypeError("argc must be a set, not list")
        if not isinstance(kwargs['argv'], set):
            raise TypeError("argv must be a set, not list")
        if not isinstance(kwargs['params'], list):
            raise TypeError("params must be a list, not set")
        
        if len(kwargs) != 3:
            raise ValueError("There can be only 'argc', 'argv', and 'params' arguments to the function")
        
        return self.__commands[name].call(kwargs['argc'], kwargs['argv'], kwargs['params'])