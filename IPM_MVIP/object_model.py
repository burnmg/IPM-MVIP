class UnknownEquationPair:  # a pair structure of Equation

    def __init__(self, equation1, equation2):
        self.equation1 = equation1
        self.equation2 = equation2


class UnknownEquation:  # This class represents the equations contains the unobservable variables.

    def __init__(self, dependent_variable, o_fragment=None):

        if not o_fragment:
            o_fragment = []
        # assert isinstance(o_fragment, str)
        self.dependent_variable = dependent_variable  # one string
        self.rates = []  # a list of Rates
        self.o_fragment = o_fragment  # a string

    def __eq__(self, other):

        assert isinstance(other, UnknownEquation)

        if self.dependent_variable != other.dependent_variable:
            return False

        if len(self.rates) != len(other.rates):
            return False

        if self.o_fragment != other.o_fragment:
            return False

        for rate in self.rates:
            if rate not in other.rates:
                return False

        return True

    def contain_rate(self, rate):
        if rate in self.rates:
            return True
        else:
            return False

    def add_rate(self, rate):
        assert isinstance(rate, Rate)
        if rate in self.rates:
            raise NameError('The new added rate ',  rate.variables, ' is already in the equation')
        self.rates.append(rate)

    def add_rates(self, rates):
        for rate in rates:
            self.add_rate(rate)

    def remove_rate(self, rate):
        assert isinstance(rate, Rate)
        self.rates.remove(rate)

    def remove_all_rates(self):
        self.rates = []

    def set_o_fragment(self, variable):

        assert isinstance(variable, str)
        self.o_fragment = variable

    def to_string(self):
        string = 'd' + self.dependent_variable + ' = '

        rates_string = ''
        for rate in self.rates:
            rates_string += rate.to_string() + ' '
        string += rates_string

        unobservable_rate = 'z'
        unobservable_rate += '*' + self.o_fragment

        string += unobservable_rate

        return string


class Rate:
    def __init__(self, variables):
        self.variables = variables  # a list of string

    def __eq__(self, other):
        assert isinstance(other, Rate)
        if len(self.variables) != len(other.variables):
            return False

        for item in self.variables:
            if item not in other.variables:
                return False
        return True

    def find_variable(self, target):
        for item in self.variables:
            if item == target:
                return True

        return False

    def to_string(self):
        string = ''
        for var in self.variables:
            string += var + '*'

        string_list = list(string)
        if len(string_list) > 0:
            del string_list[len(string_list) - 1]  # remove the last *
            string = "".join(string_list)

        return string
