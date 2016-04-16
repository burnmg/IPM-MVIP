from IPM_MVIP.data_loader import *

from IPM_MVIP.coefficient_optimiser2 import *

wb = load_workbook('../../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')


# upper derivative
# rates = R3
rates1 = load_rates(ws, ['O5:O103'])
# der = dx2
der1 = load_single_variable(ws, 'V5:V103')
# divs =
divs1 = load_o_fragment(ws, ['H5:H103'])


# lower derivative
# rates = R3 R4
rates2 = load_rates(ws, ['O5:O103', 'P5:P103'])
# der = dx3
der2 = load_single_variable(ws, 'W5:W103')
# divs = x3
divs2 = load_o_fragment(ws, ['I5:I103'])

run(1000, rates1, rates2, der1, der2, divs1, divs2)
print '\n'
# run(1000, rates2, rates1, der2, der1, divs2, divs1)

