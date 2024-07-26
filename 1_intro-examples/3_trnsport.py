'''
A Transportation Problem (TRNSPORT)

This problem finds a least cost shipping schedule that meets
requirements at markets and supplies at factories.

Dantzig, G B, Chapter 3.3. In Linear Programming and Extensions.
Princeton University Press, Princeton, New Jersey, 1963.
'''

from gamspy import Container, Set, Parameter, Variable, Equation, Model, Sense, VariableType, Sum

# Data
supply_locs = ['seattle', 'san-diego']
demand_locs = ['new-york', 'chicago', 'topeka']
distances = {
    ("seattle", "new-york"): 2.5,
    ("seattle", "chicago"): 1.7,
    ("seattle", "topeka"): 1.8,
    ("san-diego", "new-york"): 2.5,
    ("san-diego", "chicago"): 1.8,
    ("san-diego", "topeka"): 1.4,
}
capacities = {'seattle': 350, 'san-diego': 600}
demands = {'new-york': 325, 'chicago': 300, 'topeka': 275}

def triples(pairs_to_val):
    return [[pair[0],pair[1],v] for pair,v in pairs_to_val.items()]

# Model
m = Container()
i = Set(m, records=supply_locs)
j = Set(m, records=demand_locs)
a = Parameter(m, domain=i, records=capacities.items())
b = Parameter(m, domain=j, records=demands.items())
d = Parameter(m, domain=[i,j], records=triples(distances))

c = Parameter(m, domain=[i,j])
c[i,j] = 90 * d[i,j] / 1000 # shipment costs from i to j proportional to distance

x = Variable(m, domain=[i,j], type=VariableType.POSITIVE)
supply = Equation(m, domain=i, definition=Sum(j, x[i,j]) <= a[i])
demand = Equation(m, domain=j, definition=Sum(i, x[i,j]) >= b[j])

transport = Model(m, name='transport', equations=[supply,demand],
                  sense=Sense.MIN, objective=Sum((i,j), c[i,j]*x[i,j]))

# Solve and display
res = transport.solve()
print(res)
for pair,amount in x.toDict().items():
    from_,to = pair
    print(f'{from_} -> {to}: {amount}')