import pathlib
import os
import random

INSTANCE_BLACK_LIST = ['toy']

instances_path = pathlib.Path(__file__).parent.parent / 'instances'


def analyze_benchmark_instances():
    benchmark_info = {}
    for file in os.listdir(instances_path):
        if file not in INSTANCE_BLACK_LIST:
            with open(instances_path / file) as f:
                vertex_line = f.readlines()[2]
                vertex_number = int(vertex_line.split(':')[1])
                if vertex_number not in benchmark_info:
                    benchmark_info[vertex_number] = 0
                benchmark_info[vertex_number] += 1

    print(benchmark_info)


def select_benchmark_instances():
    instances_by_size = {}
    for file in os.listdir(instances_path):
        if file not in INSTANCE_BLACK_LIST:
            with open(instances_path / file) as f:
                vertex_line = f.readlines()[2]
                vertex_number = int(vertex_line.split(':')[1])
                if vertex_number not in instances_by_size:
                    instances_by_size[vertex_number] = []
                instances_by_size[vertex_number].append(file)

    selected_instances = {}
    for instance_size, possible_instances in instances_by_size.items():
        selected_instances[instance_size] = set()
        while len(selected_instances[instance_size]) < 5:
            instance_index = random.randint(0, len(possible_instances) - 1)
            selected_instances[instance_size].add(possible_instances[instance_index])

    print(selected_instances)


def main():
    analyze_benchmark_instances()
    select_benchmark_instances()


if __name__ == '__main__':
    main()