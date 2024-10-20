from spreadsheets.base.cells import select, embed, watch
from spreadsheets.base import rules, Spreadsheets


sheets = Spreadsheets(dynamic=True, char_width=10)

sheets.execute(
    select('B1').set_val(20)
)

sheets.execute(
    select('B2').set_val(100) # for filling one cells set_val is used
)

sheets.execute(
    # for settings any formulas or conditions embed is used
    embed('B3').conditional(
        watch('B2'), 
        ('B2 * B1 > 2000', 1000),
        ('B2 * B1 != 2000', 500),
        default=20 # the result should be 20, as the multiplication of B1 and B2 gives exactly 2000
    ) # watch is used to indicate that cell needs to change whenever dependent value changes, otherwise change will be applied only once (when setting this value)
)

sheets.execute(
    select('B4').set_val('Some string')
)

sheets.execute( # this will always monitor value of B1 and double it 
    select('B5').set_val(watch('B2'))
)

sheets.printf()

sheets.execute(
    select('B1').set_val(30)
) # nothing should change as actually nothing has changed to a virtual memo in condition of B3

sheets.printf()

# but if changing B2.... It should trigger change!
sheets.execute(
    select('B2').set_val(95)
)

sheets.printf()