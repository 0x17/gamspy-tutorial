import sys
from gamspy import Container, Set, Alias, Equation, Sum, Model, Problem, Sense, Variable, Ord, Parameter, Card, \
    VariableType

locs = ['A', 'B', 'C', 'D']

adj_mx = [
    [0, 2, 4, 4],
    [2, 0, 2, 2],
    [4, 2, 0, 2],
    [4, 2, 2, 0]
]
dists = [[i_name, j_name, adj_mx[i][j]]
         for i, i_name in enumerate(locs)
         for j, j_name in enumerate(locs)
         if i != j]

m = Container()

i = Set(m, 'i', records=locs)
j = Alias(m, 'j', alias_with=i)
d = Parameter(m, 'd', domain=[i, j], records=dists)
x = Variable(m, 'x', domain=[i, j], type=VariableType.BINARY)
u = Variable(m, 'u', domain=i, type=VariableType.POSITIVE)

leave_once = Equation(m, 'leave_once', domain=i)
enter_once = Equation(m, 'enter_once', domain=j)
mtz = Equation(m, 'mtz', domain=[i, j])

leave_once[i] = Sum(j.where[Ord(i) != Ord(j)], x[i, j]) == 1
enter_once[j] = Sum(i.where[Ord(i) != Ord(j)], x[i, j]) == 1
mtz[i, j].where[(Ord(i) != Ord(j)) & (Ord(i) > 1) & (Ord(j) > 1)] = u[i] - u[j] + Card(i) * x[i, j] <= Card(i) - 1

model = Model(m, 'tsp',
              equations=[leave_once, enter_once, mtz],
              problem=Problem.MIP,
              sense=Sense.MIN,
              objective=Sum((i, j), d[i, j] * x[i, j]))
res = model.solve(output=sys.stdout)

arcs = [k for k, v in x.toDict().items() if v > 0.0]
print(arcs)
print(u.toDict())
print(mtz.records)
