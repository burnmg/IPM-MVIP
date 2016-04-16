

from IPM_MVIP.coefficient_optimiser2 import *

wb = load_workbook('../../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')

# lower equation
# der: dx2
der1 = load_single_variable(ws, 'V5:V103')

# rates: R2
rates1 = load_rates(ws, ['N5:N103'])

# divs: x2
divs1 = load_o_fragment(ws, ['H5:H103'])


# lower equation
# der: dx4
der2 = load_single_variable(ws, 'X5:X103')

# rates: R5
rates2 = load_rates(ws, ['Q5:Q103'])

# divs: x4
divs2 = load_o_fragment(ws, ['J5:J103'])


for i in range(100):

    res = run(1, rates1, rates2, der1, der2, divs1, divs2)
    if res[0]: break
