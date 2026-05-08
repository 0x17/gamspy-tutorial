# Derived from model contributed by Dr. Alireza Soroudi
# For more details please refer to Chapter 2 (Gcode2.3), of the following book:
# Soroudi, Alireza. Power System Optimization Modeling in GAMS. Springer, 2017.
from gamspy import Container, Variable, Equation, Model
m = Container()
x, y = Variable(m), Variable(m, type="binary")
eq1 = Equation(m, definition=-3 * x + 2 * y >= 1)
eq2 = Equation(m, definition=-8 * x + 10 * y <= 10)
mod = Model(m, equations=m.getEquations(),
            problem="mip", sense="max",
            objective=x+y)
x.up[...] = 0.3
mod.solve()
print(f'Objective = {mod.objective_value}')
print(f'x: {x.toValue():.4f}, y: {y.toValue():.4f}')