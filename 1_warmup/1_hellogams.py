import gamspy as gp
with gp.Container() as c:
    x = gp.Variable()
    m = gp.Model(equations=[gp.Equation(definition=x==23)],
             sense="min", objective=x)
    m.solve()
    print(f'Optimal = {x.toValue()}')