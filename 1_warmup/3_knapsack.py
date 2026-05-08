import gamspy as gp

# Data
items = ['a','b','c', 'd']
profits = dict(a=3, b=5, c=2, d=4)
weights = dict(a=4, b=10, c=8, d=5)
capacity = 15

# Model
with gp.Container() as m:
    i = gp.Set(records=items)
    p = gp.Parameter(domain=i, records=profits.items())
    w = gp.Parameter(domain=i, records=weights.items())
    c = gp.Parameter(records=capacity)
    x = gp.Variable(domain=i, description="choice", type="binary")
    cap_restr = gp.Equation()
    cap_restr[...] = gp.Sum(i, w[i] * x[i]) <= c
    knapsack = gp.Model(
        equations=m.getEquations(),
        problem="mip",
        sense="max",
        objective=gp.Sum(i, p[i] * x[i]),
    )
    # Solve and display solution
    knapsack.solve()
    print(f"Utility of choice = {knapsack.objective_value}")
    print(f"Chosen items = {[ item for item, indicator in x.toList() if indicator > 0 ]}")
