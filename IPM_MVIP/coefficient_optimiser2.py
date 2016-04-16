from scipy.optimize import minimize
import random
from sklearn import preprocessing
from data_loader import *

"""
3.0
Fix the optimisation function.
Print coefficient for two equations separately.
Change div into obervable fragement
"""


def objf(theta, rates1, rates2, der1, der2, o_fragment1, o_fragment2):
    # all list must be numpy array.

    # theta1: vector of coefficients for first derivative
    # theta2: vector of coefficients for second derivative
    # rates1: All rates' data appearing in the numerator. m*n matrix. One row is sum of all rates in one time step.
    # rates2: All rates' data appearing in the denominator. m*n matrix. One row is sum of all rates in one time step.
    # der1: vector of data for first derivative. One element is an entry for one time step
    # der2: vector of data for second derivative. One element is an entry for one time step
    # o_fragment1: All div appearing in the numerator.  m*n matrix. One row is sum of all observable fragment of missing rate in one time step.
    # o_fragment2: All div appearing in the denominator. m*n matrix. One row is sum of all observable fragment of missing rate in one time step.

    theta1 = theta[0:len(rates1[0])]
    theta2 = theta[len(rates1[0]):]
    ratio_list = []
    for i in range(len(der1)):
        ratio_list.append(((der1[i] - sum(theta1 * rates1[i])) / sum(o_fragment1[i]))
                          /
                          ((der2[i] - sum(theta2 * rates2[i])) / sum(o_fragment2[i])))


    mean = sum(ratio_list) / len(ratio_list)

    return sum(
        (((ratio_list[i] - mean) ** 2)/mean ** 2
         for i in range(len(der1))
         ))


def con(theta, rates1, rates2, der1, der2, o_fragment1, o_fragment2):
    theta1 = theta[0:len(rates1[0])]
    theta2 = theta[len(rates1[0]):]

    return sum(abs(((der1[i] - sum(theta1 * rates1[i])) / sum(o_fragment1[i])) / (
    (der2[i] - sum(theta2 * rates2[i])) / sum(o_fragment2[i]))) - 1
               for i in range(len(der1)))


def compute_constant_ratio(theta, rates1, rates2, der1, der2, o_fragment1, o_fragment2):
    theta1 = theta[0:len(rates1[0])]
    theta2 = theta[len(rates1[0]):]

    for i in range(len(der1)):
        r1 = (der1[i] - sum(theta1 * rates1[i])) / sum(o_fragment1[i])
        r2 = (der2[i] - sum(theta2 * rates2[i])) / sum(o_fragment2[i])

        print(r1 / r2)


def compute_mean_constant_ratio(theta, rates1, rates2, der1, der2, o_fragment1, o_fragment2):
    theta1 = theta[0:len(rates1[0])]
    theta2 = theta[len(rates1[0]):]

    mean = 0
    for i in range(len(der1)):
        r1 = (der1[i] - sum(theta1 * rates1[i])) / sum(o_fragment1[i])
        r2 = (der2[i] - sum(theta2 * rates2[i])) / sum(o_fragment2[i])
        mean += r1 / r2
    mean /= len(der1)

    return mean


def inducing_unobservable_variables_value(coefficients, rates, der, o_fragment):
    unobservables = []
    for i in range(len(rates)):
        unobservables.append((der[i] - sum(coefficients * rates[i])) / o_fragment[i])
    np_unobservables = np.array(unobservables)
    unobservable_values = np_unobservables.T[0]
    return unobservable_values


def run(iteration_time, rates1, rates2, der1, der2, o_fragment1, o_fragment2):
    # rates1: All rates' data appears in the numerator. m*n matrix. One row is sum of all rates in one time step.
    # rates2: All rates' data appears in the denominator. m*n matrix. One row is sum of all rates in one time step.

    success = False

    for i in range(iteration_time):
        random.seed()
        init_theta = []

        for j in range(len(rates1[0]) + len(rates2[0])):
            init_theta.append(random.uniform(-5, 5))
        bound = 5.0
        res_correct = minimize(objf, init_theta, args=(rates1, rates2, der1, der2, o_fragment1, o_fragment2),
                               method='SLSQP', jac=False,
                               options={'ftol': 1e-8, 'disp': False}, bounds=[(-bound, bound)] * len(init_theta))
        coefficients1 = res_correct.x[0:len(rates1[0])]
        coefficients2 = res_correct.x[len(rates1[0]):]
        print 'initial coefficients: ', init_theta
        print 'coefficients: ', res_correct.x
        print 'objective function cost value: ', res_correct.fun
        print 'mean of constant ratio:', compute_mean_constant_ratio(res_correct.x, rates1, rates2, der1, der2,
                                                                     o_fragment1, o_fragment2)
        # test if one coefficient is significantly smaller than other coefficients in one equation. If we detect
        # one coefficient is significantly smaller,
        # we treat this equation structure is wrong even though it has good fit.
        coefficients_ratio_threshold = 1.0/8
        exist_significant_small_coefficient = False
        for item1 in coefficients1:
            for item2 in coefficients1:
                if abs(item1/item2) < coefficients_ratio_threshold:
                    exist_significant_small_coefficient = True
                    break

        for item1 in coefficients2:
            for item2 in coefficients2:
                if abs(item1/item2) < coefficients_ratio_threshold:
                    exist_significant_small_coefficient = True
                    break
        hit_bound = False
        for item in coefficients1:
            t = item - bound
            if abs(abs(item) - abs(bound)) < 0.01:
                hit_bound = True
        for item in coefficients2:
            if abs(abs(item) - abs(bound)) < 0.01:
                hit_bound = True

        if res_correct.fun < 0.05 and not exist_significant_small_coefficient and not hit_bound:
            print "Found fitting coefficients"
            print coefficients1, coefficients2  # print coefficients for two equations separately
            print 'mean ratio: ', compute_mean_constant_ratio(res_correct.x, rates1, rates2, der1, der2, o_fragment1,
                                                              o_fragment2)
            print ''
            # print compute_constant_ratio(res_correct.x, rates1, rates2, der1, der2, div1, div2)

            success = True
            break
    if success:
        print 'constant ratio:'
        for i in range(len(der1)):
            r1 = (der1[i] - sum(coefficients1 * rates1[i])) / sum(o_fragment1[i])
            r2 = (der2[i] - sum(coefficients2 * rates2[i])) / sum(o_fragment2[i])
            print r1 / r2

        unobservable_values = inducing_unobservable_variables_value(coefficients1, rates1, der1,
                                                                    o_fragment1)
        print 'unobservable variables:'
        for j in range(len(unobservable_values)):
            print j + 1, unobservable_values[j]

        return True, coefficients1, coefficients2

    else:
        # print 'Cannot find fitting coefficients'
        return False, None, None
