from spreadsheets.base import rules, Spreadsheets
from spreadsheets.base.cells import select2D, watch, embed, select
from spreadsheets.parse import excel
from spreadsheets.scripts import execute


sheets = Spreadsheets()

sheets.cr(
    select2D('A-B:1-2').fill(excel.parse_from('./sample-excel.xlsx'))
)

sheets.cr(
    embed('B2').conditional(
        watch('A2', 'B1'),
        ('A2 == 256', rules.unchanged),
        default=execute('./script_file.ssh')
    )
)

sheets.printf()

sheets.cr(
    select('A2').modify(rules.mod.sub, 10)
)

sheets.printf()