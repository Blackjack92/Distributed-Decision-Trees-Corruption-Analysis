import os
import sys
import itertools
import random

scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
import dt_algorithm

def simple_corruption_validator(node):
    return (sum(node) / len(node)) > 0.5

def build_all_corrupted_tree_combinations(max_depth, number_of_corrupted_nodes):
    size = dt_algorithm.calculate_node_number_of_all_depths(max_depth)
    for positions in itertools.combinations(range(size), number_of_corrupted_nodes):
        p = [[0] for _ in range(size)]

        for i in positions:
            p[i] = [1]

        yield p

def build_random_corrupted_tree_combinations(max_depth, number_of_corrupted_nodes, iterations):
    size = dt_algorithm.calculate_node_number_of_all_depths(max_depth)
    for i in range(iterations):
        p = [[0] for _ in range(size)]
        for corrupted_index in random.sample(range(size), number_of_corrupted_nodes):
            p[corrupted_index] = [1]

        yield p
