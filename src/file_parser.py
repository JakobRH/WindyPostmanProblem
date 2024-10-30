import pathlib
import re

instances_path = pathlib.Path(__file__).parent.parent / 'instances'
pattern = re.compile(r'\(\s*(?P<u1>\d+),\s*(?P<u2>\d+)\)\s*coste*\s*(?P<cu1>\d+)\s*(?P<cu2>\d+)')


def parse_file(filename):
    edges = []
    vertices = set()
    with open(instances_path / filename) as f:
        lines = f.readlines()
        for line in lines[6:]:
            if line == "\n" or line == "LISTA_ARISTAS_NOREQ :\n":
                break
            match = pattern.match(line)
            edges.append((match.group('u1'), match.group('u2'), int(match.group('cu1')), int(match.group('cu2'))))
            vertices.add(match.group('u1'))
            vertices.add(match.group('u2'))

    neighbors = get_vertices_neighbours(edges)
    return {
        'edges': edges,
        'vertices': list(vertices),
        'neighbors': neighbors
    }


def get_vertices_neighbours(edges):
    result = dict()
    for edge in edges:
        v_i = edge[0]
        v_j = edge[1]

        if v_i not in result:
            result[v_i] = []

        if v_j not in result:
            result[v_j] = []

        result[v_i].append(v_j)
        result[v_j].append(v_i)

    return result