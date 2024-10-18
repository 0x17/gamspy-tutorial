# Derived from model contributed by Dr. Alireza Soroudi
# For more details please refer to Chapter 2 (Gcode2.3), of the following book:
# Soroudi, Alireza. Power System Optimization Modeling in GAMS. Springer, 2017.
from sys import stdout
from gamspy import Container, Variable, Equation, Model, Sense, VariableType, Problem
m = Container()
x = Variable(m)
y = Variable(m, type=VariableType.BINARY)
eq1 = Equation(m, definition=-3 * x + 2 * y >= 1)
eq2 = Equation(m, definition=-8 * x + 10 * y <= 10)
mod = Model(m, 'simplemip',
            equations=m.getEquations(),
            problem=Problem.MIP,
            sense=Sense.MAX,
            objective=x+y)
x.up[...] = 0.3
mod.solve(output=stdout)
def rounded(num):
    return round(num, 4)
print(f'Objective = {mod.objective_value}')
print(f'x: {rounded(x.toValue())}, y: {rounded(y.toValue())}')