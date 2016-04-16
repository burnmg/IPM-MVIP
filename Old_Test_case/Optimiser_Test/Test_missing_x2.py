
from IPM_MVIP.coefficient_optimiser2 import run
from IPM_MVIP.data_loader import *


wb = load_workbook('../../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')


# upper equation
# der: dx1
der1 = load_single_variable(ws, 'U5:U103')

# rates: R1 R22
rates1 = load_rates(ws, ['M5:M103', 'T5:T103'])

# divs: x2
divs1 = load_o_fragment(ws, ['G5:G103'])


# lower equation
# der: dx3
der2 = load_single_variable(ws, 'W5:W103')

# rates: R4 R22
rates2 = load_rates(ws, ['P5:P103', 'T5:T103'])

# divs: x3
divs2 = load_o_fragment(ws, ['I5:I103'])


for i in range(100):
    print i
    res = run(1, rates1, rates2, der1, der2, divs1, divs2)
    print '\n'
    if res[0]: break
