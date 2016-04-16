from Optimiser.Data_Loader import *

from Optimiser.Coefficient_Optimiser import *

wb = load_workbook('../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')

# upper equation
# der: dx1
der1 = load_der(ws, 'U5:U103')

# rates: R1 R2
rates1 = load_rates(ws, ['M5:M103', 'N5:N103'])

# divs: x1
divs1 = load_divs(ws, ['G5:G103'])


# lower equation
# der: dx2
der2 = load_der(ws, 'V5:V103')

# rates: R2
rates2 = load_rates(ws, ['N5:N103'])

# divs: x2
divs2 = load_divs(ws, ['H5:H103'])


run(1-0, rates1, rates2, der1, der2, divs1, divs2)
print '\n'
run(20, rates2, rates1, der2, der1, divs2, divs1)