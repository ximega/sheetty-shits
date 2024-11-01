"""This module contains main Spreadsheets class that everything is instantiated from

class Spreadsheets: used to create, delete, and do other manipulations with it
"""


import sys
import time
from typing import Self, Literal, Any
from .classes import Cell, Address
from .cells import Executable, select
from .rules import Commands, ExecutableInstructions, SelectDirection
from ..libs.utils import void, CellValues
from ..dynamic.command import Console


type PositiveInteger = int
type EmptyLiteral = Literal['']


class Spreadsheets:
    """
    Class for instantiating a new spreadsheets table
    """
    __slots__ = [
        '__dynamic',
        '__char_width', '__cols_width',
        '__limits',
        '__content',
        '__max_address',
        'console'
    ]

    def __new__(cls, *,
            char_width: PositiveInteger = 7,
            col_max: PositiveInteger = 1000,
            row_max: PositiveInteger = 1000,
        ) -> Self:

        return super().__new__(cls)

    def __init__(self, *,
            char_width: PositiveInteger = 7,
            col_max: PositiveInteger = 1000,
            row_max: PositiveInteger = 1000,
        ) -> None:

        self.__dynamic: bool = False
        self.__char_width: PositiveInteger = char_width
        self.__limits: dict[str, int] = {'col': col_max, 'row': row_max}
        self.__content: dict[Address, Cell] = {}
        self.__max_address: Address | None = None
        self.__cols_width: dict[str, int] = {}
        self.console: Console = Console(self)

    def enable_dynamic(self) -> Self:
        """Enables to run dynamic commands in an internal console
        """
        self.__dynamic = True
        self.console = Console(self) # type: ignore
        return self

    def limits_dict(self) -> dict[str, int]:
        """Returns limits as a dict
        """
        return self.__limits

    def limits(self) -> str:
        """Gives information about spreadsheets limits
        """
        return f"col: {self.__limits['col']}\nrow: {self.__limits['row']}"

    def __corner_address(self) -> Address:
        """Return the most bottom and right value in the spreadsheets.
        Used to find the width and height for formatting spreadsheets

        Returns:
            _Cell: the cell that is in corner.
        """
        if self.__max_address is None:
            raise ValueError("Spreadsheets are empty. Cannot use corner_value method")

        return self.__max_address

    def __try_settings_new_max_cell(self, address: Address) -> None:
        if self.__max_address is None:
            self.__max_address = address
            return

        if (address.n_col >= self.__max_address.n_col) and (address.row >= self.__max_address.row):
            self.__max_address = address
            return
        elif (address.n_col >= self.__max_address.n_col) and (address.row <= self.__max_address.row):
            self.__max_address = Address(Address.get_col_by_num(address.n_col), self.__max_address.row, self.__limits)
            return
        elif (address.n_col <= self.__max_address.n_col) and (address.row >= self.__max_address.row):
            self.__max_address = Address(self.__max_address.col, address.row, self.__limits)

    def resize(self, name: str, new_value: int) -> None:
        """Changes the char width of the spreadsheets

        Args:
            name (str): the column name
            new_value (int): the value to be set
        """
        self.__cols_width[name] = new_value

    def add(self, cell: Cell) -> None:
        """Adds an object to the contents of a spreadsheets

        Args:
            cell (Cell): the object of Cell that is wanted to be put at a particular address

        Raises:
            ValueError: If there is already an object at the address of the cell
        """
        if cell.address in self.__content:
            raise ValueError("There is already an object at the address")

        self.__content[cell.address] = cell

        self.__try_settings_new_max_cell(cell.address)

    def __fadd(self, cell: Cell) -> None:
        """A forceful version of self.add()"""
        self.__content[cell.address] = cell

        self.__try_settings_new_max_cell(cell.address)

    def __execute_filling(self, dct: dict[str, CellValues]) -> None:
        for address_str, value in dct.items():
            col, row = Address.split_address_str(address_str)
            address = Address(col, row, self.limits_dict())
            try:
                self.__fadd(Cell(
                    address,
                    value.__class__,
                    value
                ))
            except KeyError:
                pass

    def get(self, address: Address) -> Cell:
        """Gets the value out of contents of a spreadsheets. Raises ValueError if nothing is found
        """
        try:
            return self.__content[address]
        except KeyError as exc:
            raise ValueError(f"There is no object at this address: {address}") from exc

    def execute(self, executable: Executable) -> None:
        """Executes a command over CellManager and changes the contents of a spreadsheets
        """
        match executable.instruction:
            case ExecutableInstructions.Fill:
                self.__execute_filling(executable.kwargs['content'])

    def __make_rows(self) -> tuple[str, str]:
        EMPTY_SPACE = ' '
        # two empty chars from each side (left and right).
        # This also equals len(str(V_SEP)) - len(str(V_SEP.strip()))
        V_SEP_SIDE_SPACE = 2
        H_SEP = '-'
        H_S_SEP = '='
        X_SEP = '+'

        max_col: str = self.__corner_address().col
        max_row: int = self.__corner_address().row

        max_row_len: int = len(str(max_row))

        cols: list[str] = Address.iterate_cols_until(max_col)

        h_cols: list[str] = []
        for col in cols:
            number_of_dashes: int = self.__char_width + V_SEP_SIDE_SPACE
            try:
                number_of_dashes: int = self.__cols_width[col] + V_SEP_SIDE_SPACE
            except KeyError:
                pass
            h_cols.append(H_SEP * number_of_dashes)

        H_ROW: str = EMPTY_SPACE \
                     + X_SEP + H_SEP*(max_row_len+V_SEP_SIDE_SPACE) \
                     + X_SEP + X_SEP.join(h_cols) \
                     + X_SEP

        h_s_cols: list[str] = []
        for col in cols:
            number_of_dashes: int = self.__char_width + V_SEP_SIDE_SPACE
            try:
                number_of_dashes: int = self.__cols_width[col] + V_SEP_SIDE_SPACE
            except KeyError:
                pass
            h_s_cols.append(H_S_SEP * number_of_dashes)

        H_S_ROW: str = EMPTY_SPACE \
                       + X_SEP + H_SEP*(max_row_len+V_SEP_SIDE_SPACE) \
                       + X_SEP + X_SEP.join(h_s_cols) \
                       + X_SEP

        return (H_ROW, H_S_ROW)

    def printf(self) -> None:
        """Formats and prints spreadsheets to a console

        Returns:
            str: the formatted spreadsheets
        """
        EMPTY_SPACE = ' '
        V_SEP = ' | '
        V_S_SEP = ' ‖ '
        NEW_LINE = '\n'

        parts: list[str] = []

        max_col: str = self.__corner_address().col
        max_row: int = self.__corner_address().row

        max_row_len: int = len(str(max_row))

        cols: list[str] = Address.iterate_cols_until(max_col)

        if len(cols) == 0:
            raise ValueError("The spreadsheets are empty, nothing to show")

        H_ROW, H_S_ROW = self.__make_rows()

        # first row with columns =============================================================
        a_col_rest_space: int = self.__char_width - len(str(cols[0]))
        try:
            a_col_rest_space: int = self.__cols_width[cols[0]] - len(str(cols[0]))
        except KeyError:
            pass

        cols_formatted: list[str] = []
        cols_formatted.append(
            V_SEP \
            + EMPTY_SPACE*max_row_len \
            + V_S_SEP \
            + str(cols[0]) + EMPTY_SPACE*(a_col_rest_space) \
            + V_SEP
        )

        for col in cols[1:]:
            rest_space: int = self.__char_width - len(str(col))
            try:
                rest_space: int = self.__cols_width[col] - len(str(col))
            except KeyError:
                pass

            if rest_space < 0:
                max_width: int = self.__char_width
                try:
                    max_width: int = self.__cols_width[col]
                except KeyError:
                    pass
                cols_formatted.append(str(col)[0:max_width])
                continue

            cols_formatted.append(str(col) + EMPTY_SPACE*rest_space + V_SEP)

        parts.append(
            H_ROW \
            + NEW_LINE \
            + ''.join(
                [
                    *cols_formatted
                ]
            ) \
            + NEW_LINE \
            + H_S_ROW \
            + NEW_LINE
        )
        # =====================================================================================

        # rest of the rows
        T_H_ROW = H_ROW[0:5] + V_S_SEP.strip() + H_ROW[6:] # changing "+" cross-section to "||" for rows

        for row in range(1, max_row+1):
            row_rest_space: int = max_row_len - len(str(row))

            local_parts: list[str] = []

            for col in cols:
                value: EmptyLiteral | Cell = ''
                try:
                    value = self.__content[Address(col, row, self.__limits)]
                except KeyError:
                    pass

                value_rest_space: int = self.__char_width - len(str(value))
                try:
                    value_rest_space: int = self.__cols_width[col] - len(str(value))
                except KeyError:
                    pass

                if value_rest_space < 0:
                    max_width: int = self.__char_width
                    try:
                        max_width: int = self.__cols_width[col]
                    except KeyError:
                        pass
                    local_parts.append(str(value)[0:max_width] + V_SEP)
                    continue

                local_parts.append(str(value) + EMPTY_SPACE*value_rest_space + V_SEP)

            parts.append(
                V_SEP \
                + str(row) + EMPTY_SPACE*row_rest_space \
                + V_S_SEP \
                + ''.join(local_parts)
                + NEW_LINE \
            )

        print(parts[0] + (T_H_ROW + NEW_LINE).join(parts[1:]))

    def __raise_empty_arg_error(self, *args: str | list[str] | range) -> None:
        raise ValueError(f"{args[1]} must be empty at {args[0]} command")

    def __check_allowed_args(self, command: Commands, **kwargs: str | list[str] | int) -> None:
        if kwargs['name'] == command['name']:
            for key, arg in kwargs.items():
                if key == 'params':
                    continue

                cmd_value: str | list[str] | range = command[key]

                if isinstance(arg, str) and isinstance(cmd_value, str):
                    if arg not in cmd_value:
                        self.__raise_empty_arg_error(command['name'], key)
                if isinstance(arg, list) and isinstance(cmd_value, list):
                    if len(set(arg)) - len(set(cmd_value)) > 0:
                        self.__raise_empty_arg_error(command['name'], key)


    def __ask_input_command(self) -> tuple[Commands, list[str], list[str], list[str], dict[str, str | list[str]]]:
        args: list[str] = input('$: ').strip().split(' ')

        if len(args) == 0:
            raise ValueError("No command provided")

        cmd: str = args[0]
        argc: list[str] = [] # single -
        argv: list[str] = [] # double --
        params: list[str] = []
        command: Commands = Commands.Nil

        try:
            command: Commands = getattr(Commands, cmd[0].capitalize() + cmd[1:])
        except AttributeError as exc:
            raise ValueError(f"Unknown command: {cmd}") from exc
        except IndexError:
            return (Commands.Nil, [], [], [], {'name': '', 'argc': [], 'argv': [], 'params': []})

        if len(args) > 1:
            for arg in args[1:]:
                if arg[0] == '-' and arg[1] != '-':
                    argcs: str | list[str] | range = command['argc']
                    if not isinstance(argcs, list):
                        raise ValueError("command['argc'] must be a list")
                    if arg not in argcs:
                        raise ValueError(f"Unrecognized argc: {arg}")
                    argc.extend(list(arg[1:]))
                elif arg[0] == '-' and arg[1] == '-':
                    argvs: str | list[str] | range = command['argv']
                    if not isinstance(argvs, list):
                        raise ValueError("command['argv'] must be a list")
                    if arg not in argvs:
                        raise ValueError(f"Unrecognized argv: {arg}")
                    argv.append(arg[2:])
                else:
                    params.append(arg)

            param_range: str | list[str] | range = command['param_req']
            if not isinstance(param_range, range):
                raise ValueError(f"{command} param requirement is not type of range()")

            if len(params) not in param_range:
                raise ValueError("The command does not meat param amount")

        dargs: dict[str, str | list[str]] = {
            'name': cmd,
            'argc': argc,
            'argv': argv,
            'params': params
        }

        return (
            command,
            argc,
            argv,
            params,
            dargs
        )

    def __check_is_command(self, params: list[str]) -> None:
        for param in params:
            if param in Commands:
                raise ValueError(f"Parameter cannot equal a command name: {param}")
            
    def __return_cells_through_selection(self, address_str: str, direction: SelectDirection, length: int) -> tuple[list[Cell], str]:
        cells: list[Cell] = []

        for address_str_fromselect in select(address_str, direction, length).addresses_str:
            try:
                col_str, row_int = Address.split_address_str(address_str_fromselect)
                cell: Cell = self.__content[Address(col_str, row_int, self.limits_dict())]
                cells.append(cell)
            except KeyError:
                pass

        prev_print: str = ", ".join([str(cell.address) for cell in cells])

        return (cells, prev_print)

    def run(self) -> None:
        """Runs a dynamic version of spreadsheets with a console for dynamic commands
        """
        if not self.__dynamic:
            raise PermissionError("Spreadsheets are not dynamic, can't use .run() method")

        prev_print: str = str()
        prev_params: dict[str, Any] = {}

        try:
            while True:
                try:
                    self.printf()
                    print('\n\n' + prev_print)

                    cmd, argc, argv, params, dargs = self.__ask_input_command()

                    self.__check_allowed_args(Commands.Exit, **dargs)

                    try:
                        selected_cells = prev_params['selected_cells']
                        void(selected_cells)

                        if cmd not in (Commands.Get): # NOTE: add other command that use Commands.Select # type: ignore
                            prev_print = f"Cannot use {cmd['name']} following select. Please use deselect to use {cmd['name']}"
                            continue
                    except KeyError:
                        pass

                    match cmd:
                        case Commands.Nil:
                            prev_print: str = "Cannot have an empty command"
                            continue
                        case Commands.Exit:
                            print('Finishing...')
                            time.sleep(2)
                            sys.exit()
                        case Commands.Col:
                            self.__check_is_command(params)

                            if not Address.is_valid_col(params[0]):
                                prev_print: str = "First param must be column"
                                continue

                            try:
                                width: int = int(params[1])

                                self.resize(params[0], width)

                                prev_print: str = f"Width for column {params[0]} set to {width} chars"
                                continue
                            except ValueError:
                                prev_print: str = "Second param must be an integer"
                                continue
                        case Commands.Select:
                            if len(argc) > 1:
                                prev_print: str = "Select command cannot wark with more than one argument. Only one can be provided"
                                continue

                            if not argc:
                                # if argc is empty, then selects each one by one
                                continue

                            match argc[0]: # type: ignore
                                case '1':
                                    # -1
                                    if len(params) > 2:
                                        prev_print: str = f"Cannot have more than two params in '-1' mode: {cmd['name']}"
                                        continue

                                    if len(argv) != 1:
                                        prev_print: str = f"The number of directions must equal one: {cmd['name']}"
                                        continue

                                    address_str: str = params[0]

                                    if not Address.is_valid_address_str(address_str, (self.__corner_address().col, self.__corner_address().row)):
                                        prev_print: str = f"The address param at index 0 is invalid: {cmd['name']}"
                                        continue

                                    try:
                                        if not params[1].isdigit():
                                            prev_print: str = f"The length param at index 1 is invalid and must be an integer: {cmd['name']}"
                                            continue
                                    except IndexError:
                                        prev_print: str = f"Did not receive the length param: {cmd['name']}"
                                        continue

                                    length: int = int(params[1])

                                    match argv[0]: # type: ignore
                                        case 'l':
                                            prev_params['selected_cells'], prev_print = self.__return_cells_through_selection(address_str, SelectDirection.Left, length)
                                            continue
                                        case 'r':
                                            prev_params['selected_cells'], prev_print = self.__return_cells_through_selection(address_str, SelectDirection.Right, length)
                                            continue
                                        case 'u':
                                            prev_params['selected_cells'], prev_print = self.__return_cells_through_selection(address_str, SelectDirection.Up, length)
                                            continue
                                        case 'd':
                                            prev_params['selected_cells'], prev_print = self.__return_cells_through_selection(address_str, SelectDirection.Down, length)
                                            continue

                                case '2':
                                    # -2
                                    if len(params) > 2:
                                        prev_print: str = f"Cannot have more than two params in '-2' mode: {cmd['name']}"
                                        continue

                                    if len(argv) != 2:
                                        prev_print: str = f"The number of directions must equal two: {cmd['name']}"
                                        continue

                                    directions: dict[str, None | str] = {'x': None, 'y': None}
                                    for arg in argv:
                                        if (directions['x'] is not None) or (directions['y'] is not None):
                                            prev_print: str = f"Cannot have two direction in one axis: {cmd}"
                                            continue

                                        if arg in ('l', 'r'):
                                            pass

                                        if arg in ('u', 'd'):
                                            pass

                        case Commands.Get:
                            try:
                                prev_print: str = ", ".join([str(cell.value()) for cell in prev_params['selected_cells']]) # type: ignore
                                continue
                            except KeyError:
                                prev_print: str = f"Must select at least one cell before using: {cmd['name']}"
                                continue
                        case Commands.Deselect:
                            try:
                                prev_print = f"Deselected {len(prev_params['selected_cells'])} cells: {cmd['name']}"
                                del prev_params['selected_cells']
                                continue
                            except KeyError:
                                prev_print = f"Nothing to deselect: {cmd['name']}"
                                continue
                        case _: # type: ignore
                            if cmd in Commands:
                                prev_print: str = f"Not implemented command: {cmd['name']}"
                                continue

                            prev_print: str = f"Unknown command: {cmd['name']}"
                            continue

                except ValueError as exc:
                    prev_print = exc.args[0]
                    continue
        except (EOFError, KeyboardInterrupt):
            print("\nProcess finished")
