from gamspy import Container, Ord, Parameter, Set
m = Container()
i = Set(m, 'i', records=[f"i{i+1}" for i in range(5)])
a, b = Parameter(m, 'a', domain=[i]), Parameter(m, 'b', domain=[i])
a[i] = Ord(i)
b[i.lag(2, "linear")] = a[i]
print(f'{a.records}\n{b.records}')