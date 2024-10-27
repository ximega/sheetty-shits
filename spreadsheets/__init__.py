"""
The packages allows to create, manage, and parse information in a format of spreadsheets

The spreadsheets are created through importing Spreadsheets class from spreadsheets.base
The command are executed through .execute() method

Learn more at DOCUMENTATION.md and see real examples at examples/
"""

__all__ = [
    'Spreadsheets',
]


from .base.main import Spreadsheets
