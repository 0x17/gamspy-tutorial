from gamspy import Container, Equation, Model, Parameter, Problem, Sense, Set, Sum, Variable, VariableType

items = ['a','b','c', 'd']
profits = dict(a=3, b=5, c=2, d=4)
weights = dict(a=4, b=10, c=8, d=5)
capacity = 15

m = Container()
i = Set(m, "i", records=items)
p = Parameter(m, "p", domain=i, records=profits.items())
w = Parameter(m, "w", domain=i, records=weights.items())
c = Parameter(m, "c", records=capacity)
x = Variable(m, "x", domain=i, description="choice", type=VariableType.BINARY)

cap_restr = Equation(m, 'cap_restr')
cap_restr[...] = Sum(i, w[i] * x[i]) <= c

knapsack = Model(
    m, name="knapsack",
    equations=m.getEquations(),
    problem=Problem.MIP,
    sense=Sense.MAX,
    objective=Sum(i, p[i] * x[i]),
)

knapsack.solve()
print(f"Utility of choice = {knapsack.objective_value}")
print(f"Chosen items = {[ item for item, indicator in x.toList() if indicator > 0 ]}")
