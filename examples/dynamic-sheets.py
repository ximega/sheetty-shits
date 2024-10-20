from spreadsheets.base.cells import select
from spreadsheets.base import rules, Spreadsheets

sheets = Spreadsheets(dynamic=True)

sheets.console.add_handler(
    name='double',
    args=[
        rules.console.cells,
    ],
    docs='Doubles the values of integers'
)

sheets.execute(
    select('A-D:1').descending(10)
)

sheets.execute(
    select('A-D:1').copy('2-6', axis=rules.axis.Y) # so it select downwards (by y axis)
)

sheets.run()