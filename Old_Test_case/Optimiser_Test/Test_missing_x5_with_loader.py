
from IPM_MVIP.coefficient_optimiser2 import run
from IPM_MVIP.data_loader import *


wb = load_workbook('../../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')


# upper derivative
# rates
rates1 = load_rates(ws, ['S5:S103'])
# der
der1 = load_single_variable(ws, 'Z5:Z103')
# divs
divs1 = load_o_fragment(ws, ['L5:L103'])


# lower derivative
# rates
rates2 = load_rates(ws, ['P5:P103'])
# der
der2 = load_single_variable(ws, 'X5:X103')
# divs
divs2 = load_o_fragment(ws, ['J5:J103'])

run(1000, rates2, rates1, der2, der1, divs2, divs1)