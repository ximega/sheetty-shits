"""Contains commands that allow to manage and execute changes to a spreadsheets
"""



__all__= [
    'select',
    'CellManager',
]


from typing import Self
from .classes import Address
from .rules import SelectFormats, SelectDirection, ExecutionCommands


class CellManager:
    """Manages cells and contains a list of them
    """

    __slots__ = [
        '__content',
        'addresses_str',
        'select_mode',
        'command_from'
    ]

    def __new__(cls) -> Self:
        return super().__new__(cls)

    def __init__(self) -> None:
        return
    
    def set_selection(self, addresses_str: str | list[str] | tuple[str, int, SelectDirection | tuple[SelectDirection, SelectDirection]], select_format: SelectFormats) -> Self:
        """A list of addresses from select command
        """
        self.command_from = ExecutionCommands.Select
        self.addresses_str = addresses_str
        self.select_mode: SelectFormats = select_format

        return self
    
    def __str__(self) -> str:
        try:
            return f"<CellManager command: {self.command_from}>"
        except AttributeError:
            return "<CellManager empty>"

def select(address_range: str, /, direction: SelectDirection | tuple[SelectDirection, SelectDirection] | None = None, number: int | None = 0) -> CellManager:
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
            else:
                select_format: SelectFormats = SelectFormats.OneDim


        if Address.is_valid_address_str(address_range, None):
            select_format: SelectFormats = SelectFormats.ZeroDim

        match select_format:
            case SelectFormats.ZeroDim:
                return CellManager().set_selection(
                    address_range,
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
        
        if isinstance(direction, tuple):
            select_format: SelectFormats = SelectFormats.Rectangle

        
        if direction in SelectDirection:
            select_format: SelectFormats = SelectFormats.Line

        if select_format == SelectFormats.Nil:
            raise ValueError(INVALID_CELL_ERR_TEXT)
        
        if number is None:
            raise TypeError("number must be of type int")
        
        return CellManager().set_selection(
            (address_range, number, direction),
            select_format
        )