from declasp.declare.constraint import Constraint, ActivityVariable


class Model:
    def __init__(self):
        self.constraints = list()
        self.variables = list()

    @property
    def has_variables(self):
        return len(self.variables) > 0

    def add_constraint(self, c: Constraint):
        self.constraints.append(c)
        for arg in c.arguments:
            if isinstance(arg, ActivityVariable):
                self.variables.append(arg)

    def reify(self):
        for constraint in self.constraints:
            yield from constraint.reify()

        for variable in self.variables:
            yield from variable.reify()
