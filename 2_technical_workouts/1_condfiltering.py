from gamspy.math import mod
import gamspy as gp
elems = [f"i{i+1}" for i in range(5)]
with gp.Container() as m:
    i = gp.Set(records=elems)
    a = gp.Parameter(domain=[i], records=[[e, i+1] for i,e in enumerate(elems)])
    b = gp.Parameter(domain=[i])
    b[i].where[(mod(a[i], 2) == 0) | (a[i] == 1)] = 23
    print(f'{a.records}\n{b.records}')