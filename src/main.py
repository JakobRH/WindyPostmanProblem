import pathlib
import sys

from ortools.sat.python import cp_model

import file_parser
import solver
benchmarks_path = pathlib.Path(__file__).parent.parent / 'benchmarks'

if __name__ == '__main__':
    # file_to_print = open(benchmarks_path / 'benchmarks_?.txt', 'w')
    file_to_print = sys.stdout
    # print('model parameter settings:', file=file_to_print)
    # print('     variable_selection_strategy: X', file=file_to_print)
    # print('     domain_reduction_strategy: X', file=file_to_print)
    # print('     num_workers: 1', file=file_to_print)
    # print('     max_time_in_seconds : 300 (5min)', file=file_to_print)
    # print('     upper bound: X', file=file_to_print)
    # instances = ['WA0555', 'WA0561', 'WB0542', 'WA1032', 'WA1035', 'WA1042', 'WA1545', 'WB1545', 'WB1555', 'WA2032', 'WA2061', 'WB2031', 'WA3031', 'WA3041', 'WA3052']
    instances = ['toy']
    for instance_name in instances:
        print(f'START instance: {instance_name}', file=file_to_print)
        instance = file_parser.parse_file(instance_name)
        print(f'     {instance_name} FIRST RUN', file=file_to_print)
        solver.solve(instance, file_to_print)
        #print(f'     {instance_name} SECOND RUN', file=file_to_print)
        #solver.solve(instance, file_to_print)
        # print(f'     {instance_name} THIRD RUN', file=file_to_print)
        # solver.solve(instance, file_to_print)
    file_to_print.close()
