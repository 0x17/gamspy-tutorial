from gamspy import Container, Model, Variable, Equation, Sense
from sys import stdout
m = Container()
x = Variable(m, 'x')
e1 = Equation(m, 'e1', definition=x >= 10)
e2 = Equation(m, 'e2', definition=x <= 5)
mod = Model(m, 'mymodel', equations=m.getEquations(), sense=Sense.MAX, objective=x)
res = mod.solve(output=stdout, solver='CPLEX', solver_options=dict(iis=1))