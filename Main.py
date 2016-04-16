'''
# test case. Missing x4
eq1 = UnknownEquation('x3', [], [])
eq2 = UnknownEquation('x5', [], [])
known_rates = [Rate(['x2', 'x3']), Rate(['x1', 'x3']), Rate(['x1', 'x2']), Rate(['x5', 'x6'])]

data_locations = {

    'x1': 'G5:G103',
    'x2': 'H5:H103',
    'x3': 'I5:I103',
    'x4': 'J5:J103',
    'x5': 'K5:K103',
    'x6': 'L5:L103',
    'a': 'D5:D103',
    # z is a variable with value 1 on every time step.
    # z can be plugged into "observable variables contained in the unobservable rate" term.
    # If z is plugged in this term, it represents there is no observable variables contained in the unobservable rate.

    'dx1': 'U5:U103',
    'dx2': 'V5:V103',
    'dx3': 'W5:W103',
    'dx4': 'X5:X103',
    'dx5': 'Y5:Y103',
    'dx6': 'Z5:Z103',
}

wb = load_workbook('../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')

variables = ['x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'a']

if run(100, ws, eq1, eq2, known_rates, data_locations, variables, 2, 4):
    print 1
'''

'''
# test case. Missing x5
eq1 = UnknownEquation('x4')
eq2 = UnknownEquation('x6')

known_rates = [Rate(['x1']),
               Rate(['x1', 'x2']),
               Rate(['x1', 'x2']),
               Rate(['x1', 'x3']),
               Rate(['x2', 'x3']),
               Rate(['x3', 'x4'])]

data_locations = {

    'x1': 'G5:G103',
    'x2': 'H5:H103',
    'x3': 'I5:I103',
    'x4': 'J5:J103',
    'x5': 'K5:K103',
    'x6': 'L5:L103',
    'a': 'D5:D103',
    # z is a variable with value 1 on every time step.
    # z can be plugged into "observable variables contained in the unobservable rate" term.
    # If z is plugged in this term, it represents there is no observable variables contained in the unobservable rate.

    'dx1': 'U5:U103',
    'dx2': 'V5:V103',
    'dx3': 'W5:W103',
    'dx4': 'X5:X103',
    'dx5': 'Y5:Y103',
    'dx6': 'Z5:Z103',
}
wb = load_workbook('../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')

variables = ['x1', 'x2', 'x3', 'x4', 'x6']


if run(100, ws, eq1, eq2, known_rates, data_locations, variables, 2, 4, mode=2):
    print 1
'''


# test case. Missing x2
eq1 = UnknownEquation('x1')
eq2 = UnknownEquation('x3')

known_rates = [
               Rate(['x3', 'x4'])]

data_locations = {

    'x1': 'G5:G103',
    'x2': 'H5:H103',
    'x3': 'I5:I103',
    'x4': 'J5:J103',
    'x5': 'K5:K103',
    'x6': 'L5:L103',
    'a': 'D5:D103',
    # z is a variable with value 1 on every time step.
    # z can be plugged into "observable variables contained in the unobservable rate" term.
    # If z is plugged in this term, it represents there is no observable variables contained in the unobservable rate.

    'dx1': 'U5:U103',
    'dx2': 'V5:V103',
    'dx3': 'W5:W103',
    'dx4': 'X5:X103',
    'dx5': 'Y5:Y103',
    'dx6': 'Z5:Z103',
}
wb = load_workbook('../data.xlsx')
ws = wb.get_sheet_by_name('SUMMARY')

variables = ['x1', 'x2', 'x3', 'x4', 'x6']
eq1

success, eq1, eq2, coef1, coef2 = run(100, ws, eq1, eq2, known_rates, data_locations, variables, 2, 4, mode=2)

if success:
    print eq1.to_string()
    print eq2.to_string()
    print coef1
    print coef2