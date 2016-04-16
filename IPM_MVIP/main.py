import itertools
import model_search_module2
import time


def run(iteration_time, variables, target_variables, known_rates, work_sheet, data_locations,
        right_equation_pair=None, test_mode=False):

    start_time = time.time()
    equation_pairs = itertools.combinations(target_variables, 2)

    for equation_pair in equation_pairs:
        var1 = equation_pair[0]
        var2 = equation_pair[1]

        '''
        def run(, equation1, equation2, known_rates, data_locations, variables, target_variables,
        rate_max_length, equation_max_length, mode=2):'''

        res = model_search_module2.run(iteration_time, right_equation_pair, work_sheet, var1, var2, known_rates, data_locations, variables,
                                       target_variables, 2, 4, test_mode=test_mode)
        if res[0]:

            print 'total time cost: ', time.time() - start_time
            # if the induced equation are correct
            if test_mode:
                if res[5]:
                    print 'This test returned Correct Result'
                    return True
                else:
                    print 'This test returned Wrong Result'
                    return False

    print 'total time cost: ', time.time() - start_time
    return False
