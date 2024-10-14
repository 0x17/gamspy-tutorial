from gamspy import Container, Equation, Model, Parameter, Problem, Sense, Set, Sum, Variable, VariableType
# Model
m = Container()
i = Set(m, "i")
p, w, c = Parameter(m, "p", domain=i), Parameter(m, "w", domain=i), Parameter(m, "c")
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
# Data
i.setRecords(['a','b','c', 'd']) # items
p.setRecords(dict(a=3, b=5, c=2, d=4).items()) # profits
w.setRecords(dict(a=4, b=10, c=8, d=5).items()) # weights
c.setRecords(15) # capacity
# Solve and display solution
knapsack.solve()
print(f"Utility of choice = {knapsack.objective_value}")
print(f"Chosen items = {[ item for item, indicator in x.toList() if indicator > 0 ]}")