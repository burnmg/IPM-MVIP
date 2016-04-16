
from IPM_MVIP.coefficient_optimiser2 import run
from IPM_MVIP.data_loader import *

wb = load_workbook('../../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')

# upper equation
# der: dx1
der1 = load_single_variable(ws, 'U5:U103')

# rates: R1 R2
rates1 = load_rates(ws, ['M5:M103', 'N5:N103'])

# divs: x1
divs1 = load_o_fragment(ws, ['G5:G103'])


# lower equation
# der: dx4
der2 = load_single_variable(ws, 'X5:X103')

# rates: R5
rates2 = load_rates(ws, ['Q5:Q103'])

# divs: x4
divs2 = load_o_fragment(ws, ['J5:J103'])


run(100, rates1, rates2, der1, der2, divs1, divs2)