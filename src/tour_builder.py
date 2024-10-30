import numpy as np


def build_tour(edge_variables, solver):
    edge_list = {}
    sub_cycles = []
    # copy only traversed edges
    for edge in edge_variables.keys():
        val = solver.Value(edge_variables[edge])
        if val > 0:
            edge_list[edge] = val

    temp_vertex = list(edge_list.keys())[0][0]  # start with first edge/vertex
    temp_tour = [temp_vertex]
    while sum(edge_list.values()) > 0:  # continue until every edge is traversed
        next_edge = ()
        for edge in edge_list.keys():
            if edge[0] == temp_vertex:
                next_edge = edge
                temp_vertex = edge[1]
                if temp_vertex in temp_tour:  # when we have a subcycle, save it and remove it from temp_tour
                    index = temp_tour.index(temp_vertex)
                    sub_cycles.append(temp_tour[index:])
                    temp_tour = temp_tour[:index + 1]
                    temp_vertex = temp_tour[-1]
                else:
                    temp_tour.append(temp_vertex)
                break
        if next_edge == ():  # if stuck at one vertex after subtour. but there are still edges,start with a new one
            temp_vertex = list(edge_list.keys())[0][0]
            temp_tour = [temp_vertex]
        else:
            edge_list[next_edge] -= 1
            if edge_list[next_edge] == 0: edge_list.pop(next_edge)  # remove if no traverses no more

    result_tour = []
    on_tour = np.full(len(sub_cycles), False)  # keep track fo which cycles were already visited (are part of the tour)
    connect_cycles_to_tour(result_tour, sub_cycles[0], sub_cycles, 0, on_tour)
    return result_tour


def connect_cycles_to_tour(result_tour, temp_cycle, sub_cycles, index, on_tour):
    on_tour[sub_cycles.index(temp_cycle)] = True
    start = temp_cycle[index]

    for i in range(len(temp_cycle)):
        vertex = temp_cycle[index + i]
        in_another_tour = False

        for sub_cycle in sub_cycles:
            if not on_tour[sub_cycles.index(sub_cycle)] and vertex in sub_cycle:
                in_another_tour = True
                connect_cycles_to_tour(result_tour, sub_cycle, sub_cycles, sub_cycle.index(vertex), on_tour)

        if not in_another_tour:
            result_tour.append(vertex)

        if index + i + 1 == len(temp_cycle): index = index - len(temp_cycle)
    result_tour.append(start)
