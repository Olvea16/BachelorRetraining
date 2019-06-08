from random import choice, random

class Parameter:
    def __init__(self, default_value = None, change_chance = None, choices = []):
        assert ((change_chance is None) or (0 <= change_chance <= 1)), 'Chance should be between 0 and 1 if specified.'
        assert (change_chance == None or (default_value != None and choices != []))
        assert isinstance(choices, list)

        if default_value != None:
            self.default_value = default_value
        else:
            self.change_chance = 1
            self.default_value = None

        if choices != []:
            self.choices = choices
        else:
            self.change_chance = 0
        
        if default_value != None and choices != []:
            self.change_chance = change_chance

        pass

    def set_default(self, new_default):
        self.default_value = new_default

    def set_choices(self, new_choices):
        assert isinstance(new_choices, list)
        self.choices = new_choices

    def set_chance(self, new_chance):
        assert (0 <= new_chance <= 1), 'Chance should be between 0 and 1.'
        self.change_chance = new_chance
        
    def get_permutations(self):
        if self.default_value is not None:
            return len(self.choices) + 1
        else:
            return len(self.choices)

    def add_choices(self, new_choices):
        if isinstance(new_choices, list):
            self.choices += new_choices
        else:
            self.choices.append(new_choices)

    def sample(self):
        assert (self.change_chance == 0 or len(self.choices) != 0), 'Chance should be 0 with no choices.'
    
        if random() < self.change_chance:
            value = choice(self.choices)
        else:
            value = self.default_value

        return value


class ParameterGenerator:
    def __init__(self, unique=False):
        self.parameters = {}

        pass

    def add_value(self, parameter_name, default_value = None, change_chance = None, choices = []):
        assert isinstance(parameter_name, str), 'Parameter name not string object.'
        try: choices = list(choices)
        except: pass
        assert isinstance(choices, (list)),'Choices should be iterable.'

        par = Parameter(default_value, change_chance, choices)
        self.parameters[parameter_name] = par

    def get_permutations(self):
        result = 1
        for key in self.parameters:
            result *= self.parameters[key].get_permutations()
        return result

    # This implementation is based on randomness so the time complexity is terrible with a lot of permutations if the argument amount is near the limit.
    def sample(self, amount=1, unique=False):
        assert (len(self.parameters) != 0)
        assert (unique and amount <= self.get_permutations()), 'Cannot generate {} permutations, max permutations is {}.'.format(amount, self.get_permutations())
        
        parameters = []
        for i in range(0, amount):
            parameter_set = {}
            while (parameter_set == {}) or (parameter_set in parameters and unique):
                for key in self.parameters:
                    parameter_set[key] = self.parameters[key].sample()
            parameters.append(parameter_set)
        return parameters
