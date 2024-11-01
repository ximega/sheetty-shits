from typing import Any
from spreadsheets.base import Spreadsheets
from spreadsheets.base.classes import Address, Cell
from spreadsheets.libs import Array, Integer
from spreadsheets.dynamic.rules import params
from spreadsheets.base.cells import select


sheets: Spreadsheets = Spreadsheets().enable_dynamic()

def array_append(sp: Spreadsheets, argc: set[str], argv: set[str], param_types: list[Any]) -> str:
    address_str = param_types[0]
    col, row = Address.split_address_str(address_str)
    address = Address(col, row, sp.limits_dict())
    value = param_types[1]
    cell: Cell = sp.get(address)
    if cell.type_equals(Array):
        cell.append(value)
    else:
        raise TypeError("Cannot use with anything else than arrays")
    return f"Appended a new element to {address}"

sheets.console.add_handler(
    name='append',
    argc={},
    argv={},
    param_types=[
        params.Address,
        params.Integer or params.String or params.Float
    ],
    docs='Add any value to a global list of all (added) values',
    handler=array_append
)

sheets.execute(
    select('A1').fill(Array(Integer, [Integer(x) for x in range(1, 5)]))
)

sheets.run()