"""Contains commands that allow to manage and execute changes to a spreadsheets
"""



__all__= [
    'select',
    'Executable'
]


from typing import Self, Any
from ..libs.utils import CellValues
from ..libs.integer import Integer
from .classes import Address
from .rules import SelectFormats, SelectDirection, ExecutionCommands, ExecutableInstructions


class Executable:
    """Cooked executable instructions for the execute method in a spreadsheets
    """
    def __init__(self, instruction: ExecutableInstructions, **kwargs: Any) -> None:
        self.instruction: ExecutableInstructions = instruction
        self.kwargs: dict[str, Any] = kwargs

class CellManager:
    """Manages cells and contains a list of them
    """

    __slots__ = [
        'addresses_str',
        'select_mode',
        'command_from'
    ]
    
    def set_selection(self, addresses_str: list[str], select_format: SelectFormats) -> Self:
        """A list of addresses from select command
        """
        self.command_from: ExecutionCommands = ExecutionCommands.Select
        self.addresses_str: list[str] = addresses_str
        self.select_mode: SelectFormats = select_format

        return self
    
    def __str__(self) -> str:
        try:
            return f"<CellManager command: {self.command_from}>"
        except AttributeError:
            return "<CellManager empty>"
        
    def fill(self, *values: CellValues) -> Executable:
        """Fills the selected area
        """
        if self.command_from != ExecutionCommands.Select:
            raise TypeError("Cannot fill values, as the selection was not applied beforehand")
        
        if len(values) != len(self.addresses_str):
            raise ValueError("The number of values that fill the addresses cannot be lower or higher than of the number of addresses")
        
        dct: dict[str, CellValues] = {}
        for index, value in enumerate(values):
            dct[self.addresses_str[index]] = value
        return Executable(
            ExecutableInstructions.Fill,
            content = dct
        )
    
    def ascending_int(self, *, start: int, step: int, stop: int | None = None) -> Executable:
        """Increases the value of the cell starting at 'start' 
        and increasing value by 'step' at each operation
        until it reaches stop, the value of stop will be included as well
        """
        if (stop is not None) and (start > stop):
            raise ValueError("stop point cannot be lower than start")

        if self.command_from != ExecutionCommands.Select:
            raise TypeError("Cannot fill values, as the selection was not applied beforehand")
        
        dct: dict[str, CellValues] = {}

        for index, address_str in enumerate(self.addresses_str):
            value: int = start + step*index
            if (stop is not None) and (stop < value):
                break
            dct[address_str] = Integer(value)

        return Executable(
            ExecutableInstructions.Fill,
            content = dct
        )
    
    def descending_int(self, *, start: int, step: int, stop: int | None = None) -> Executable:
        """Decreases the value of the cell starting at 'start' 
        and decreasing value by 'step' at each operation
        until it reaches stop, the value of stop will be included as well
        """
        if (stop is not None) and (start < stop):
            raise ValueError("stop point cannot be higher than start")
        
        if self.command_from != ExecutionCommands.Select:
            raise TypeError("Cannot fill values, as the selection was not applied beforehand")

        dct: dict[str, CellValues] = {}

        for index, address_str in enumerate(self.addresses_str):
            value: int = start - step*index
            if (stop is not None) and (stop < value):
                break
            dct[address_str] = Integer(value)

        return Executable(
            ExecutableInstructions.Fill,
            content = dct
        )

def select(
        address_range: str, 
        /, 
        direction: SelectDirection | tuple[SelectDirection, SelectDirection] | None = None, 
        number: int | tuple[int, int] | None = None
    ) -> CellManager:
    """Select a singe or list of cells and allows managing over it

    Args:
        address_range (str): the address(-es) that are to be selected
        direction (SelectDirection): the direction from a particular point to be set from onwards to (direction)

    Returns:
        CellManager: simply a list of cells that can be managed
    """
    DASH = '-'
    COLON = ':'
    INVALID_CELL_ERR_TEXT = "Invalid cell address, learn more about cell address for select in docs"

    if (direction is None and number is not None) or (direction is not None and number is None):
        raise ValueError("Direction and number must be provided at the same time")

    select_format: SelectFormats = SelectFormats.Nil

    # singular and multi-dimensional cells
    if direction is None:
        parts: list[str] = address_range.split(COLON)

        # lines and rectangular shapes
        if DASH in address_range:
            if len(parts) != 2:
                raise ValueError(INVALID_CELL_ERR_TEXT)

            first_part, second_part = parts

            chars: list[str] = first_part.split(DASH)
            for char in chars:
                for splt in list(char):
                    if splt not in Address.valid_chars:
                        raise ValueError(INVALID_CELL_ERR_TEXT)

            digits: list[str] = second_part.split(DASH)
            for digit in digits:
                for splt in list(digit):
                    if not splt.isdigit():
                        raise ValueError(INVALID_CELL_ERR_TEXT)

            if DASH in first_part and DASH in second_part:
                select_format: SelectFormats = SelectFormats.TwoDim
            elif DASH in first_part or DASH in second_part:
                select_format: SelectFormats = SelectFormats.OneDim
            elif Address.is_valid_address_str(address_range, None):
                select_format: SelectFormats = SelectFormats.ZeroDim

        match select_format:
            case SelectFormats.ZeroDim:
                return CellManager().set_selection(
                    [address_range],
                    select_format
                )
            case SelectFormats.OneDim:
                addresses_str: list[str] = []

                if DASH in parts[0]:
                    first_col, second_col = parts[0].split(DASH)
                    for col_n in range(Address.get_col_num(first_col), Address.get_col_num(second_col)+1):
                        addresses_str.append(f"{Address.get_col_by_num(col_n)}{parts[1]}")
                    
                elif DASH in parts[1]:
                    first_row, second_row = parts[1].split(DASH)
                    for row in range(int(first_row), int(second_row)+1):
                        addresses_str.append(f"{parts[0]}{row}")

                return CellManager().set_selection(
                    addresses_str,
                    select_format
                )
            case SelectFormats.TwoDim:
                addresses_str: list[str] = []

                first_col, second_col = parts[0].split(DASH)
                first_row, second_row = parts[1].split(DASH)
                for col_n in range(Address.get_col_num(first_col), Address.get_col_num(second_col)+1):
                    for row in range(int(first_row), int(second_row)+1):
                        addresses_str.append(f"{Address.get_col_by_num(col_n)}{row}")

                return CellManager().set_selection(
                    addresses_str,
                    select_format
                )
                
            case SelectFormats.Nil:
                raise ValueError(INVALID_CELL_ERR_TEXT)
    # the handling with directions:
    else:
        if not Address.is_valid_address_str(address_range, None):
            raise ValueError(INVALID_CELL_ERR_TEXT)
        
        if isinstance(direction, tuple) and isinstance(number, tuple):
            select_format: SelectFormats = SelectFormats.Rectangle
        elif isinstance(direction, SelectDirection) and isinstance(number, int):
            select_format: SelectFormats = SelectFormats.Line
        else:
            raise TypeError("Undefined select format for a select function")
        
        addresses_str: list[str] = []

        col, row = Address.split_address_str(address_range)
        col_n: int = Address.get_col_num(col)

        match select_format:
            case SelectFormats.Rectangle:
                if (not isinstance(direction, tuple)) or (not isinstance(number, tuple)):
                    raise TypeError("Direction provided was identified as tuple and select format was set to rectangle")

                first_dir, second_dir = direction

                match first_dir:      
                    case SelectDirection.Left:
                        for nw_col_n in range(col_n-number[0], col_n+1):
                            match second_dir:
                                case SelectDirection.Up:
                                    for nw_row in range(row-number[1], row+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case SelectDirection.Down:
                                    for nw_row in range(row, row+number[1]+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case _:
                                    raise ValueError("Cannot choose two direction in the same axis")
                    case SelectDirection.Right:
                        for nw_col_n in range(col_n, col_n+number[0]+1):
                            match second_dir:
                                case SelectDirection.Up:
                                    for nw_row in range(row-number[1], row+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case SelectDirection.Down:
                                    for nw_row in range(row, row+number[1]+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case _:
                                    raise ValueError("Cannot choose two direction in the same axis")
                    case SelectDirection.Up:
                        for nw_row in range(row-number[0], row+1):
                            match second_dir:
                                case SelectDirection.Left:
                                    for nw_col_n in range(col_n-number[1], col_n+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case SelectDirection.Right:
                                    for nw_col_n in range(col_n, col_n+number[1]+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case _:
                                    raise ValueError("Cannot choose two direction in the same axis")
                    case SelectDirection.Down:
                        for nw_row in range(row, row+number[0]+1):
                            match second_dir:
                                case SelectDirection.Left:
                                    for nw_col_n in range(col_n-number[1], col_n+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case SelectDirection.Right:
                                    for nw_col_n in range(col_n, col_n+number[1]+1):
                                        addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{nw_row}")
                                case _:
                                    raise ValueError("Cannot choose two direction in the same axis")
            case SelectFormats.Line:
                if not isinstance(number, int):
                    raise TypeError("Direction provided was identified as integer and select format was set to line")
                
                match direction:
                    case SelectDirection.Left:
                        for nw_col_n in range(col_n-number, col_n+1):
                            addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{row}")
                    case SelectDirection.Right:
                        for nw_col_n in range(col_n, col_n+number+1):
                            addresses_str.append(f"{Address.get_col_by_num(nw_col_n)}{row}")
                    case SelectDirection.Up:
                        for nw_row in range(row-number, row+1):
                            addresses_str.append(f"{col}{nw_row}")
                    case SelectDirection.Down:
                        for nw_row in range(row, row+number+1):
                            addresses_str.append(f"{col}{nw_row}")
                    case _:
                        raise TypeError("No other direction is available to usage")
        
        return CellManager().set_selection(
            addresses_str,
            select_format
        )
    