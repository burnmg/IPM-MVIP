from itertools import combinations
from object_model import *
from data_loader import *
import coefficient_optimiser2
import time
import random


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
    for var in equation1.o_fragment:
        o_fragment1_locations.append(data_locations[var])

    o_fragment2_locations = []
    for var in equation2.o_fragment:
        o_fragment2_locations.append(data_locations[var])

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
    for rate in candidate_rates:
        if rate in inferred_rates:
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


def run(iteration_time, ws, equation1, equation2, known_rates, data_locations, variables, target_variables,
        rate_max_length, equation_max_length, mode=2):
    # data_location: a dictionary contains the location of data in .xlsx file
    # variables: a list of strings containing the name of variables involving in the system
    assert isinstance(equation1, UnknownEquation)
    assert isinstance(equation2, UnknownEquation)
    assert isinstance(data_locations, dict)

    # build a pair of equations with inferred_rates
    inferred_rates1 = infer_rates(known_rates, equation1.dependent_variable)
    inferred_rates2 = infer_rates(known_rates, equation2.dependent_variable)

    equation1.add_rates(inferred_rates1)
    equation2.add_rates(inferred_rates2)

    # Initialise all candidate partial equations that can be plugged on the right side of the current equation pairs
    # if the current equation pair is not correct.
    # We have built two partial equations based on the inferred rates, but this pair does not guarantee of having the right structures.
    # If the structures are not right, it means that it needs more rates to be plugged on the right side.
    # In this step, it initialise all possible partial equations that can be plugged on the right side of current pair of equations given all variables.
    # 'partial equation' is a tuple of rates.
    candidate_rates1 = build_candidate_rates(variables, target_variables, known_rates, inferred_rates1, rate_max_length)
    candidate_rates2 = build_candidate_rates(variables, target_variables, known_rates, inferred_rates2, rate_max_length)
    '''
    # remove all inferred rate from the candidate rate list
    for rate in inferred_rates1:
        candidate_rates1.remove(rate)

    for rate in inferred_rates2:
        candidate_rates2.remove(rate)
    '''
    candidate_partial_equations1 = build_all_candidate_partial_equations(candidate_rates1,
                                                                         equation_max_length - len(inferred_rates1) - 1)
    t = equation_max_length - len(inferred_rates1) - 1
    candidate_partial_equations2 = build_all_candidate_partial_equations(candidate_rates2,
                                                                         equation_max_length - len(inferred_rates2) - 1)
    # candidate_partial_equations1 = [[]] + sorted(candidate_partial_equations1, key=lambda equation: len(equation))
    # candidate_partial_equations2 = [[]] + sorted(candidate_partial_equations2, key=lambda equation: len(equation))

    random.shuffle(candidate_partial_equations1)
    random.shuffle(candidate_partial_equations2)
    candidate_partial_equations1 = [[]] + candidate_partial_equations1
    candidate_partial_equations2 = [[]] + candidate_partial_equations2
    if mode == 2:
        # build all candidate observable fragment
        candidate_o_fragments1 = target_variables
        candidate_o_fragments2 = target_variables

    else:
        candidate_o_fragments1 = ['a']
        candidate_o_fragments2 = ['a']


    search_space_size = len(candidate_partial_equations1) * len(candidate_partial_equations2) * len(
        candidate_o_fragments1) * len(candidate_o_fragments2)
    print 'search space size: ', search_space_size
    print '\nPlugging new rates'

    for i in range(iteration_time):
        print 'iteration_time: ', i
        # plug different rates in the "observable independent terms". Start from no plugged rate
        for candidate_partial_equation1 in candidate_partial_equations1:
            equation1.remove_all_rates()
            equation1.add_rates(inferred_rates1)
            if candidate_partial_equation1 == [] and equation1.rates == []: continue
            equation1.add_rates(candidate_partial_equation1)
            for candidate_partial_equation2 in candidate_partial_equations2:
                equation2.remove_all_rates()
                equation2.add_rates(inferred_rates2)
                if candidate_partial_equation2 == [] and equation2.rates == []: continue
                equation2.add_rates(candidate_partial_equation2)

                # According to the assumption,
                # if the rate composed by two equations' variables appear sin one equation,
                # it must appear in the other equations.
                # Therefore, we do not need to test the combinations violating the above rule.

                # plug different variables in the term "observable variables contained in the unobservable rate"
                for candidate_fragment1 in candidate_o_fragments1:
                    for candidate_fragment2 in candidate_o_fragments2:
                        equation1.o_fragment = [candidate_fragment1]
                        equation2.o_fragment = [candidate_fragment2]

                        # load data for equations
                        der1_data, der2_data, rates_data1, rates_data2, o_fragment1_data, o_fragment2_data = \
                            load_data_for_equations_pairs(ws, data_locations, equation1, equation2)
                        # run the optimisation program
                        print '\n'
                        print 'equation 1: ', equation1.to_string()
                        print 'equation 2: ', equation2.to_string()

                        start_time = time.time()
                        (success, coef1, coef2) = coefficient_optimiser2.run(1, rates_data1, rates_data2, der1_data,
                                                                            der2_data,
                                                                            o_fragment1_data,
                                                                            o_fragment2_data)
                        print 'unit_time_cost: ', time.time() - start_time
                        if success:
                            return True, equation1, equation2, coef1, coef2

    return False, None, None, None, None
