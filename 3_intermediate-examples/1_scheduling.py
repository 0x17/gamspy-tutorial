from os import makedirs
from sys import stdout

from gamspy import Container, Equation, Model, Parameter, Problem, Sense, Set, Sum, Variable, VariableType, Ord, Alias

from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Dark2_5 as palette

# Input data
n_machines = 3
machines = [f'Machine {i+1}' for i in range(n_machines)]
n_jobs = 5
jobs = [f'Job {i+1}' for i in range(n_jobs)]
durations = [
    [1, 2, 3, 4, 2],
    [2, 4, 5, 7, 8],
    [3, 8, 9, 6, 4]
]
duration_triples = [
    [job,machine,durations[m][j]]
    for j, job in enumerate(jobs)
    for m, machine in enumerate(machines)
]
# loose upper bound for worst case makespan
T = sum(max(durations[m][j] for m in range(n_machines)) for j in range(n_jobs) )
periods = list(range(T))

# Model
c = Container()
j, m, t = Set(c, 'j', records=jobs), Set(c, 'm', records=machines), Set(c, 't', records=periods)
tau = Alias(c, 'tau', alias_with=t)
d = Parameter(c, 'd', domain=[j,m], records=duration_triples)
x = Variable(c, 'x', domain=[j,m,t], description='Job j starts on machine m in period t', type=VariableType.BINARY)
y = Variable(c, 'y', description='Makespan of the schedule')

each_job_once = Equation(c, 'once', domain=j, definition=Sum((m,t), x[j,m,t]) == 1, description='each job runs once on exactly one machine')
machine_cap = Equation(c, 'machine_cap', domain=[m,t], description='max. one job (simultaneously) on a specific machine at every point in time')
machine_cap[m,t] = Sum(j, Sum(tau.where[(Ord(tau) >= Ord(t) - d[j,m] + 1) & (Ord(tau) <= Ord(t))], x[j,m,tau])) <= 1
makespan = Equation(c, 'makespan', domain=j, definition=y >= Sum((m,t), x[j,m,t] * (Ord(t)+d[j,m])))

scheduling = Model(c, 'scheduling',
                   problem=Problem.MIP,
                   sense=Sense.MIN,
                   equations=c.getEquations(),
                   # minimize makespan
                   objective=y)

# Solve and visualize solution
scheduling.solve(output=stdout)

#scheduling.solve(output=stdout, solver="CPLEX", solver_options={"iis": 1})
#scheduling.compute_infeasibilities()

xd = x.toDict()
if xd: # only if feasible solution exists
    triples = [triple for triple, v in xd.items() if v > 0.0]
    for triple in triples:
        print(triple)
    assigned_machines = [m for _,m,_ in triples]
    starts = [int(t) for _,_,t in triples]
    ends = [int(t) + durations[machines.index(m)][jobs.index(j)] for j,m,t in triples ]
    tasks = dict(Machine=assigned_machines, Job=jobs, Start=starts, End=ends, Colors=palette[:len(jobs)])
    makedirs('scratch', exist_ok=True)
    output_file('scratch/schedule.html')
    p = figure(y_range=sorted(list(set(tasks['Machine'])), reverse=True), x_axis_label='Time Period', title='Machine Schedule')
    p.hbar(y='Machine', fill_color='Colors', left='Start', right='End', height=0.4, source=ColumnDataSource(tasks), legend_field='Job')
    p.legend.title = 'Job'
    p.grid.grid_line_color = None
    p.yaxis.axis_label = 'Machine'
    show(p)
