from spreadsheets.base.cells import select, select2D
from spreadsheets.base import rules, Spreadsheets

sheets = Spreadsheets()

# .execute() - is a command that sets value to a particular cell
# between() - references a range of cells
sheets.execute(
    # so 'A-D:1' is a first line from A to D cells
    select('A-D:1').ascending(1, step=2) # will increase the value of cell by 1 (default) or any specified value when selecting cells
)


sheets.execute(
    # so 'A-D:2-5' will be a rectangle of cells. When applying different dimensions it's necessary to use 2D functions
    select('A-D:2-5').mixscending2D(1, xstep=2, xscend=rules.ASCEND, ystep=1, yscend=rules.DESCEND) # will inexecuteease the value of cell by 1 (or any specified value when selecting cells) in different dimensions. Can also call by just specifying step, and it will apply to both dimensions
)

sheets.printf()
