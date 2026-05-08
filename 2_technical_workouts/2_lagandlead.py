import gamspy as gp
with gp.Container() as m:
    i = gp.Set(records=[f"i{i+1}" for i in range(5)])
    a, b = gp.Parameter(domain=[i]), gp.Parameter(domain=[i])
    a[i] = gp.Ord(i)
    b[i.lag(2, "linear")] = a[i]
    print(f'{a.records}\n{b.records}')