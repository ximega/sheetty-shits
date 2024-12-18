from spreadsheets.base.cells import select
from spreadsheets.base import Spreadsheets, rules

sheets: Spreadsheets = Spreadsheets(char_width=3).enable_dynamic()

# .execute() - is a command that sets value to a particular cell
# between() - references a range of cells
sheets.execute(
    # so 'A-D:1' is a first line from A to D cells
    select('C-D:1-9').ascending_int(start=0, step=4, stop=52) 
    # will increase the value of cell by 1 (default) or any specified value when selecting cells
)

sheets.execute(
    select('A-J:4').descending_int(start=20, step=1)
)

sheets.execute(
    select('A5', (rules.SelectDirection.Right, rules.SelectDirection.Down), (2, 3)).ascending_int(start=20, step=5)
)


# sheets.execute(
#     # so 'A-D:2-5' will be a rectangle of cells. When applying different dimensions it's necessary to use 2D functions
#     select('A-D:2-5').mixscending2D_int(1, xstep=2, xscend=rules.ASCEND, ystep=1, yscend=rules.DESCEND) 
#     # will increase the value of cell by 1 (or any specified value when selecting cells) in different dimensions. 
#     # Can also call by just specifying step, and it will apply to both dimensions
# )

sheets.run()
