from spreadsheets.base import Spreadsheets, rules
from spreadsheets.libs import Array
from spreadsheets.base.cells import select


sheets = Spreadsheets(dynamic=True)

sheets.console.add_handler(
    name='append',
    args=[
        rules.console.Integer or rules.console.String,
    ],
    docs='Add any value to a global list of all (added) values'
)

sheets.execute(
    select('A1').set_val(Array(10))
)

sheets.run()