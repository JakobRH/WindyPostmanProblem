from ortools.sat.python import cp_model
from ortools.sat.python.cp_model import LinearExpr
from timeit import default_timer as timer
from datetime import timedelta

from src.tour_builder import build_tour


def solve(instance, file_to_print):
    start_time = timer()
    model = cp_model.CpModel()

    UPPER_BOUND = 10

    max_edge_cost = max(max(instance['edges'], key=lambda item: item[3])[3], max(instance['edges'], key=lambda item: item[2])[2])
    min_edge_cost = min(min(instance['edges'], key=lambda item: item[3])[3], min(instance['edges'], key=lambda item: item[2])[2])
    edge_cost_range = max_edge_cost-min_edge_cost if max_edge_cost > min_edge_cost else 1
    domain_size_range = 7

    # create the variables
    edge_variables = {}
    for edge in instance['edges']:
        v_i = edge[0]
        v_j = edge[1]

        # scale domain-size to 3-10 depending on the cost of the edge
        upper_bound_1 = 10-int((((edge[2]-min_edge_cost)*domain_size_range)/ edge_cost_range))
        upper_bound_2 = 10-int((((edge[3] - min_edge_cost) * domain_size_range) / edge_cost_range))

        edge_variables[(v_i, v_j)] = model.NewIntVar(0, upper_bound_1, 'x_{}_{}'.format(v_i, v_j))
        edge_variables[(v_j, v_i)] = model.NewIntVar(0, upper_bound_2, 'x_{}_{}'.format(v_j, v_i))


    # add the constraints
    for edge in instance['edges']:
        v_i = edge[0]
        v_j = edge[1]

        # each edge must be taken once (independent of direction)
        model.Add(edge_variables[(v_i, v_j)] + edge_variables[(v_j, v_i)] >= 1)

    for vertex in instance['vertices']:
        ingoing_edges = [edge_variables[(x, vertex)] for x in instance['neighbors'][vertex]]
        outgoing_edges = [edge_variables[(vertex, x)] for x in instance['neighbors'][vertex]]
        model.Add(LinearExpr.Sum(ingoing_edges) == LinearExpr.Sum(outgoing_edges))

    variable_list = []
    coefficient_list = []
    for edge in instance['edges']:
        v_i = edge[0]
        v_j = edge[1]

        variable_list.append(edge_variables[(v_i, v_j)])
        coefficient_list.append(edge[2])

        variable_list.append(edge_variables[(v_j, v_i)])
        coefficient_list.append(edge[3])

    obj = LinearExpr.WeightedSum(variable_list, coefficient_list)

    # Choose right strategies
    model.AddDecisionStrategy(edge_variables.values(), cp_model.CHOOSE_MIN_DOMAIN_SIZE, cp_model.SELECT_LOWER_HALF)
    model.Minimize(obj)

    # Create solver and solve
    solver = cp_model.CpSolver()
    solver.parameters.num_workers = 1
    solver.parameters.max_time_in_seconds = 3
    status = solver.Solve(model)
    end_time = timer()

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Statistics.
        print('         Solver Statistics', file=file_to_print)
        print(f'                status   : {solver.StatusName(status)}', file=file_to_print)
        print(f'                objective value   : {solver.ObjectiveValue()}', file=file_to_print)
        print(f'                conflicts: {solver.NumConflicts()}', file=file_to_print)
        print(f'                branches : {solver.NumBranches()}', file=file_to_print)
        print(f'                solver measured wall time: {solver.WallTime()} s', file=file_to_print)
        print(f'                self measured wall time: {timedelta(seconds=end_time - start_time)} s', file=file_to_print)
        # print(f'                edge assignments: ', file=file_to_print)
        # for edge in edge_variables.keys():
            # print(f'    {edge}: {solver.Value(edge_variables[edge])}', file=file_to_print)
        print(f'                tour example: {build_tour(edge_variables, solver)}', file=file_to_print)
    else:
        print('             No solution found.', file=file_to_print)