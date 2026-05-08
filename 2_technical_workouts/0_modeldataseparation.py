from gamspy import Container, Set, Parameter, Variable, Equation, Sum, Model
# Model
with Container() as m:
    # Abstract model no data
    i = Set()
    p, w, c = Parameter(domain=i), Parameter(m, "w", domain=i), Parameter(m, "c")
    x = Variable(domain=i, description="choice", type="binary")
    cap_restr = Equation()
    cap_restr[...] = Sum(i, w[i] * x[i]) <= c
    knapsack = Model(
        equations=m.getEquations(),
        problem="mip",
        sense="max",
        objective=Sum(i, p[i] * x[i]),
    )
    # Data
    i.setRecords(['a','b','c', 'd']) # items
    p.setRecords(dict(a=3, b=5, c=2, d=4).items()) # profits
    w.setRecords(dict(a=4, b=10, c=8, d=5).items()) # weights
    c.setRecords(15) # capacity
    # Solve and display solution
    knapsack.solve()
    print(f"Utility of choice = {knapsack.objective_value}")
    print(f"Chosen items = {[ item for item, indicator in x.toList() if indicator > 0 ]}")
