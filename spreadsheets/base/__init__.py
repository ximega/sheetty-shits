"""
spreadsheets.base provides basic classes and constructors to handle basic operation on spreadsheets
"""


__all__ = [
    'Spreadsheets',
    'cells',
    'rules',
]


from .main import Spreadsheets
from . import cells, rules