from itertools import combinations
from object_model import *
from data_loader import *
import coefficient_optimiser2
import time
import copy


def find_all_candidate_products(vars, max_length):
    # One candidate product is one representing the product of multiple variables. For example (x1*x2)
    # This method will return all possible products composed by the given variables.

    # vars: list of name of variables. For example: ['x1', 'x2', 'x3']
    # max_length: max length of the candidate structure.

    candidate_products = []
    for i in range(1, max_length + 1):
        iter = combinations(vars, i)
        for element in iter:
            candidate_products.append(element)

    return candidate_products


def find_all_candidate_equations(derivative, candidate_rates, candidate_o_fragments, max_equation_rates_parts_length):
    equations = []
    candidate_equation_rates_parts = []
    for i in range(1, max_equation_rates_parts_length + 1):
        iter = combinations(candidate_rates, i)
        for element in iter:
            candidate_equation_rates_parts.append(element)

    for equation_rates_part in candidate_equation_rates_parts:
        for o_fragment in candidate_o_fragments:
            equation = UnknownEquation(derivative, equation_rates_part, o_fragment)
            equations.append(equation)
    return equations


def find_all_candidate_equation_pairs(equations1, equations2):
    equation_pairs = []
    for equation1 in equations1:
        for equation2 in equations2:
            equation_pairs.append(UnknownEquationPair(equation1, equation2))
    return equation_pairs


def infer_rates(known_rates, variable):
    # infer the rates for the equation containing unobservable variables.
    # known_rates: list of strings. rates that has been selected.
    # variable: string: name of the variable whose differential equations containing the unobservable variable

    inferred_rates = []
    for rate in known_rates:
        if rate.find_variable(variable):
            inferred_rates.append(rate)

    return inferred_rates


def load_data_for_equations_pairs(ws, data_locations, equation1, equation2):
    assert isinstance(equation1, UnknownEquation)
    assert isinstance(equation2, UnknownEquation)
    # load der
    der1_data = load_single_variable(ws, data_locations['d' + equation1.dependent_variable])
    der2_data = load_single_variable(ws, data_locations['d' + equation2.dependent_variable])

    # load rate
    rates_data1 = load_equation_rates_data(worksheet=ws, equation=equation1, locations=data_locations)
    rates_data2 = load_equation_rates_data(worksheet=ws, equation=equation2, locations=data_locations)

    # load o_fragment
    '''
    edit from here. Change argument to array on the following two lines of codes.
    '''
    o_fragment1_locations = []
    o_fragment1_locations.append(data_locations[equation1.o_fragment])

    o_fragment2_locations = []
    o_fragment2_locations.append(data_locations[equation2.o_fragment])

    o_fragment1_data = load_o_fragment(ws, o_fragment1_locations)
    o_fragment2_data = load_o_fragment(ws, o_fragment2_locations)
    return der1_data, der2_data, rates_data1, rates_data2, o_fragment1_data, o_fragment2_data


'''
def build_all_candidate_rates(vars, max_length):
    # vars: list of name of variables. For example: ['x1', 'x2', 'x3']
    # max_length: max length of the candidate structure.

    candidate_rates = []
    for i in range(1, max_length + 1):
        rate_labels = combinations(vars, i)
        for rate_label in rate_labels:
            candidate_rates.append(Rate(rate_label))

    return candidate_rates
'''


def build_candidate_rates(all_variables, target_variables, known_rates, inferred_rates, max_length):
    # all_variables: a list of all variables in the system (excluding the unobservable variable).
    # non_fitted_variable: a list of variables containing the unobservable variables in their differential equations.
    # known_rates: a list of rates that has been induced and appeared in other variables' equations.
    # inferred_rates: a list of rates that has been inferred from the known equations.
    # max_length: max length of the candidate structure.

    candidate_rates = []

    # add rates that has been induced in other equations
    candidate_rates += known_rates

    # remove all inferred rate

    for rate in inferred_rates:
        candidate_rates.remove(rate)

    # add rates not containing fitted variables.
    rates_not_containing_fitted_variables = []
    for i in range(1, max_length + 1):
        rate_strings_list = combinations(target_variables, i)
        for rate_strings in rate_strings_list:
            assert isinstance(rate_strings, tuple)
            rate = Rate(rate_strings)
            rates_not_containing_fitted_variables.append(rate)

    candidate_rates += rates_not_containing_fitted_variables

    return candidate_rates


def build_all_candidate_partial_equations(rates, max_length):
    candidate_partial_equations = []
    for i in range(1, max_length + 1):
        partial_equations = combinations(rates, i)
        for partial_equation in partial_equations:
            candidate_partial_equations.append(partial_equation)

    return candidate_partial_equations


def run(iteration_time, right_equation_pair, ws, var1, var2, known_rates, data_locations, variables, target_variables,
        rate_max_length, equation_max_length, mode=2, test_mode=False):
    # data_location: a dictionary contains the location of data in .xlsx file
    # variables: a list of strings containing the name of variables involving in the system
    assert isinstance(data_locations, dict)

    # build a pair of equations with inferred_rates
    inferred_rates1 = infer_rates(known_rates, var1)
    inferred_rates2 = infer_rates(known_rates, var2)

    # Initialise all candidate partial equations that can be plugged on the right side of the current equation pairs
    # if the current equation pair is not correct.
    # We have built two partial equations based on the inferred rates, but this pair does not guarantee of having the right structures.
    # If the structures are not right, it means that it needs more rates to be plugged on the right side.
    # In this step, it initialise all possible partial equations that can be plugged on the right side of current pair of equations given all variables.
    # 'partial equation' is a tuple of rates.
    candidate_rates1 = build_candidate_rates(variables, target_variables, known_rates, inferred_rates1, rate_max_length)
    candidate_rates2 = build_candidate_rates(variables, target_variables, known_rates, inferred_rates2, rate_max_length)


    candidate_partial_equations1 = build_all_candidate_partial_equations(candidate_rates1,
                                                                         equation_max_length - len(inferred_rates1) - 1)
    candidate_partial_equations2 = build_all_candidate_partial_equations(candidate_rates2,
                                                                         equation_max_length - len(inferred_rates2) - 1)

    '''
    candidate_partial_equations1 = [
        [Rate(['x1']),
        Rate(['x1', 'x3'])
         ]
    ]
    candidate_partial_equations2 = [
        [Rate(['x1', 'x3'])]
    ]
    '''
    # candidate_partial_equations1 = [[]] + sorted(candidate_partial_equations1, key=lambda equation: len(equation))
    # candidate_partial_equations2 = [[]] + sorted(candidate_partial_equations2, key=lambda equation: len(equation))

    if test_mode:
        candidate_partial_equations1 = [right_equation_pair.equation1.rates]
        candidate_partial_equations2 = [right_equation_pair.equation2.rates]
    else:
        candidate_partial_equations1 = [[]] + candidate_partial_equations1
        candidate_partial_equations2 = [[]] + candidate_partial_equations2

    if mode == 2:
        # build all candidate observable fragment
        if test_mode:
            candidate_o_fragments1 = [right_equation_pair.equation1.o_fragment]
            candidate_o_fragments2 = [right_equation_pair.equation2.o_fragment]
        else:
            candidate_o_fragments1 = target_variables
            candidate_o_fragments2 = target_variables
        '''
        candidate_o_fragments1 = ['x1']
        candidate_o_fragments2 = ['x3']
        '''

    else:
        candidate_o_fragments1 = ['a']
        candidate_o_fragments2 = ['a']

    equation_pairs = []
    for candidate_partial_equation1 in candidate_partial_equations1:
        equation1 = UnknownEquation(var1)
        # equation1.remove_all_rates()
        if not test_mode:
            equation1.add_rates(inferred_rates1)

        if candidate_partial_equation1 == [] and equation1.rates == []: continue
        equation1.add_rates(candidate_partial_equation1)
        for candidate_partial_equation2 in candidate_partial_equations2:
            equation2 = UnknownEquation(var2)
            if not test_mode:
                equation2.add_rates(inferred_rates2)
            if candidate_partial_equation2 == [] and equation2.rates == []: continue
            equation2.add_rates(candidate_partial_equation2)

            # According to the assumption,
            # if the rate composed by two equations' variables appears in one equation,
            # it must appear in the other equations.
            # Therefore, we do not need to test the combinations violating the above rule.
            # plug different variables in the term "observable variables contained in the unobservable rate"
            rate_composed_by_equations_variables = Rate(
                [equation1.dependent_variable, equation2.dependent_variable])
            ok_to_run = True
            if equation1.contain_rate(rate_composed_by_equations_variables) and not equation2.contain_rate(
                    rate_composed_by_equations_variables):
                ok_to_run = False
            if equation2.contain_rate(rate_composed_by_equations_variables) and not equation1.contain_rate(
                    rate_composed_by_equations_variables):
                ok_to_run = False

            # According to the assumption,
            # if the rate composed by the dependent variable of equation 1, and it appears in equation 2,
            # it must also appear in
            # equation 1. Otherwise, this pair is not valid
            rate_composed_by_equation1 = Rate([equation1.dependent_variable])

            if equation2.contain_rate(rate_composed_by_equation1) and not equation1.contain_rate(
                    rate_composed_by_equation1):
                ok_to_run = False

            # According to the assumption,
            # if the rate composed by the dependent variable of equation 2, and it appears in equation 1, i
            # t must also appear in
            # equation 2. Otherwise, this pair is not valid
            rate_composed_by_equation2 = Rate([equation2.dependent_variable])

            if equation1.contain_rate(rate_composed_by_equation2) and not equation2.contain_rate(
                    rate_composed_by_equation2):
                ok_to_run = False

            if ok_to_run:
                for candidate_fragment1 in candidate_o_fragments1:
                    for candidate_fragment2 in candidate_o_fragments2:
                        equation1.o_fragment = candidate_fragment1
                        equation2.o_fragment = candidate_fragment2
                        equation_pair = UnknownEquationPair(copy.deepcopy(equation1), copy.deepcopy(equation2))
                        equation_pairs.append(equation_pair)

    search_space_size = len(equation_pairs)
    print 'search space size: ', search_space_size

    equation_pairs = sorted(equation_pairs, key=lambda x: (len(x.equation1.rates), len(x.equation2.rates)))

    for i in range(iteration_time):
        print 'iteration_time: ', i
        for eq_pair in equation_pairs:
            assert isinstance(eq_pair, UnknownEquationPair)

            der1_data, der2_data, rates_data1, rates_data2, o_fragment1_data, o_fragment2_data = \
                load_data_for_equations_pairs(ws, data_locations, eq_pair.equation1, eq_pair.equation2)
            # run the optimisation program
            print '\n'
            print 'equation 1: ', eq_pair.equation1.to_string()
            print 'equation 2: ', eq_pair.equation2.to_string()
            assert isinstance(right_equation_pair, UnknownEquationPair)
            # Used for for testing
            if right_equation_pair.equation1 == eq_pair.equation1 and right_equation_pair.equation2 == eq_pair.equation2:
                print 'THIS IS THE RIGHT EQUATION PAIR!'
            start_time = time.time()
            (success, coef1, coef2) = coefficient_optimiser2.run(1, rates_data1, rates_data2, der1_data, der2_data,
                                                                 o_fragment1_data, o_fragment2_data)
            print 'unit_time_cost: ', time.time() - start_time

            if success:
                # For testing purpose
                # if the induced structure is correct, return is_correct as True
                is_correct = False
                if test_mode:
                    if right_equation_pair.equation1 == eq_pair.equation1 and right_equation_pair.equation2 == eq_pair.equation2:
                        is_correct = True
                return True, eq_pair.equation1, eq_pair.equation2, coef1, coef2, is_correct

    return False, None, None, None, None
