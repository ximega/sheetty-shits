"""
This module allows a user to create and manage custom command in a dynamic mode.
"""


__all__ = [
    'Console'
]



from typing import Any
from collections.abc import Callable


class _CustomCommand:
    def __init__(self,
            name: str,
            argc: set[str],
            argv: set[str],
            param_types: list[Any],
            docs: str,
            handler: Callable[[Any, set[str], set[str], list[Any]], Any],
        ) -> None:
        
        self.name: str = name
        self.argc: set[str] = argc
        self.argv: set[str] = argv
        self.param_types: list[Any] = param_types 
        self.docs: str = docs
        self.handler = handler

    def call(self, argc: set[str], argv: set[str], params: list[str]) -> str:
        """Calls a command"""
        val_argc: set[str] = argc - self.argc
        if len(val_argc) > 0:
            raise ValueError(f"Unknown value of 'argc': {val_argc}")
        val_argv: set[str] = argv - self.argv
        if len(val_argv) > 0:
            raise ValueError(f"Unknown value of 'argv': {val_argv}")
        
        for index, param in enumerate(params):
            param_type = self.param_types[index]

            match param_type:

 
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
            param_types: list[Any], 
            docs: str, 
            handler: Callable[[Any, set[str], set[str], list[Any]], Any]
        ) -> _CustomCommand: 

        """Adds a custom command"""
        command = _CustomCommand(name, argc, argv, param_types, docs, handler)

        self.__commands[name] = command
        return command
    
    def all_commands(self) -> dict[str, _CustomCommand]:
        """Lists all commands"""
        return self.__commands
    
    def call(self, name: str, **kwargs: set[str] | list[str]) -> str:
        if len(kwargs) != 3:
            raise ValueError("There can be only 'argc', 'argv', and 'params' arguments to the function")
        
        return self.__commands[name].call(kwargs['argc'], kwargs['argv'], kwargs['params'])