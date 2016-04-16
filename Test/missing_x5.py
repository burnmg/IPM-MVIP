from IPM_MVIP.object_model import *
from IPM_MVIP.data_loader import *
from IPM_MVIP import main
import time

def run():
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
    work_book = load_workbook('../data.xlsx')
    work_sheet = work_book.get_sheet_by_name('SUMMARY')

    known_rates = [Rate(['x1']),
                   Rate(['x1', 'x2']),
                   Rate(['x1', 'x3']),
                   Rate(['x2', 'x3']),
                   Rate(['x3', 'x4']),
                   ]

    variables = ['x1', 'x2', 'x3', 'x4', 'x6']
    target_variables = ['x4', 'x6']

    correct_equation1 = UnknownEquation('x4', 'x4')
    correct_equation1.add_rates(
        [
            Rate(['x3', 'x4']),
        ]
    )

    correct_equation2 = UnknownEquation('x6', 'x6')
    correct_equation2.add_rates(
        [
            Rate(['x6'])
        ])
    correct_equation_pair = UnknownEquationPair(correct_equation1, correct_equation2)

    return main.run(100, variables, target_variables, known_rates, work_sheet, data_locations, correct_equation_pair)



i = 0
total_test_time = 5
correct_count = 0
while i<5:
    print '\n\n********************************************************\n'
    print 'test: ', i
    if run():
        correct_count += 1
    i += 1

print 'in %d tests, the program succeeded %d times' % (total_test_time, correct_count)