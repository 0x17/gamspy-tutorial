import gamspy as gp
with gp.Container() as m:
    x = gp.Variable()
    m = gp.Model(equations=[gp.Equation(definition=x==23)],
             sense="min", objective=x)
    m.solve()
    m.toGams("xyz")
    print(f'Optimal = {x.toValue()}')