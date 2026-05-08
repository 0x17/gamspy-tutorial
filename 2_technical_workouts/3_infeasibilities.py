import gamspy as gp
import sys
with gp.Container() as m:
    x = gp.Variable()
    e1 = gp.Equation(definition=x >= 10)
    e2 = gp.Equation(definition=x <= 5)
    mod = gp.Model(equations=m.getEquations(), sense="max", objective=x)
    res = mod.solve(output=sys.stdout, solver='CPLEX', solver_options=dict(iis=1))