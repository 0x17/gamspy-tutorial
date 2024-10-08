from sys import stdout
from gamspy import Container, Variable, Equation, Model, Sense
m = Container()
x = Variable(m)
e = Equation(m, definition=x==23)
mod = Model(m, 'mymodel',
            equations=[e],
            sense=Sense.MIN,
            objective=x)
mod.solve(output=stdout)
print(f'Optimal = {x.toValue()}')