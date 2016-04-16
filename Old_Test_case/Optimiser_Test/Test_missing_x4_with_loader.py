
from IPM_MVIP.coefficient_optimiser2 import run
from IPM_MVIP.data_loader import *

wb = load_workbook('../../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')

# upper equation
# der: dx3
der1 = load_single_variable(ws, 'W5:W103')

# rates: R3 R22
rates1 = load_rates(ws, ['O5:O103', 'T5:T103'])

# divs: x3
divs1 = load_o_fragment(ws, ['I5:I103'])


# lower equation
# der: dx5
der2 = load_single_variable(ws, 'Y5:Y103')

# rates: R6
rates2 = load_rates(ws, ['R5:R103'])

# divs: x5
divs2 = load_o_fragment(ws, ['K5:K103'])


run(100, rates1, rates2, der1, der2, divs1, divs2)
print '\n'
# run(100, rates2, rates1, der2, der1, divs2, divs1)