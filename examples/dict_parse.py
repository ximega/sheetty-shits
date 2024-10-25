from spreadsheets.base import Spreadsheets
from spreadsheets.libs import String, Integer, Float
from spreadsheets.libs.parse import Parser
from spreadsheets.libs.utils import CellValues

dct: dict[str, list[CellValues]] = {
    'Constant name': [String('gravitational'), String('light speed')],
    'Approx. value': [Integer(10), Integer(300_000_000)],
    'Exact value': [Float(9.81), Float(299_998_346.36422)],
}

sp: Spreadsheets = Spreadsheets(dynamic=True, char_width=15)

sp: Spreadsheets = Parser(sp).from_dict(dct)

sp.run()
