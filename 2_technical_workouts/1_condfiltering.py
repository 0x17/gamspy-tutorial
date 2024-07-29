from gamspy import Container, Parameter, Set
from gamspy.math import mod
m = Container()
elems = [f"i{i+1}" for i in range(5)]
i = Set(m, 'i', records=elems)
a = Parameter(m, 'a', domain=[i], records=[[e, i+1] for i,e in enumerate(elems)])
b = Parameter(m, 'b', domain=[i])
b[i].where[(mod(a[i], 2) == 0) | (a[i] == 1)] = 23
print(f'{a.records}\n{b.records}')