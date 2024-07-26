import yaml
import folium
from sys import stdout
from gamspy import Container, Set, Alias, Equation, Sum, Model, Problem, Sense, Variable, Ord, Parameter, Card, \
    VariableType


def solve_model(locations, distances):
    m = Container()
    i = Set(m, 'i', description='locations', records=locations)
    j = Alias(m, 'j', alias_with=i)
    d = Parameter(m, 'd', description='distance', domain=[i, j], records=distances)
    x = Variable(m, name='x', domain=[i, j], type=VariableType.BINARY)
    u = Variable(m, name='u', domain=i, type=VariableType.POSITIVE)

    leave_once = Equation(m, 'leave_once', domain=i)
    enter_once = Equation(m, 'enter_once', domain=j)
    mtz = Equation(m, 'mtz', domain=[i, j])

    leave_once[i] = Sum(j.where[Ord(i) != Ord(j)], x[i, j]) == 1
    enter_once[j] = Sum(i.where[Ord(i) != Ord(j)], x[i, j]) == 1
    mtz[i, j].where[(Ord(i) != Ord(j)) & (Ord(i) > 1) & (Ord(j) > 1)] = u[i] - u[j] + Card(i) * x[i, j] <= Card(i) - 1

    tsp_mtz = Model(m, 'tsp_mtz',
                    equations=m.getEquations(),
                    problem=Problem.MIP,
                    sense=Sense.MIN,
                    objective=Sum((i, j), d[i, j] * x[i, j]))

    tsp_mtz.solve(output=stdout)
    print(f'Optimal tour has length of approx. {round(tsp_mtz.objective_value / 1000, 2)} km')
    return [k for k, v in x.toDict().items() if v > 0.0]


def main():
    with open('scratch/data.yaml', encoding='utf-8') as fp:
        data = yaml.safe_load(fp)

    arcs = solve_model(data['locations'], data['distances'])

    def succ(loc_num):
        return next(b for a, b in arcs if a == loc_num)

    location_seq = [arcs[0][0]]
    cur = arcs[0][1]
    while cur != location_seq[0]:
        location_seq.append(cur)
        cur = succ(cur)
    location_seq.append(location_seq[0])

    def get_coords(loc_num):
        return next([lat, lng] for loc, lat, lng in data['coordinates'] if loc == loc_num)

    route = [get_coords(loc_num) for loc_num in location_seq]

    m = folium.Map(location=route[0], zoom_start=13)
    for point in route:
        folium.Marker(location=point).add_to(m)
    folium.PolyLine(route, color="blue", weight=2.5, opacity=1).add_to(m)

    m.save("scratch/hitta_tsp_solution.html")


if __name__ == '__main__':
    main()
