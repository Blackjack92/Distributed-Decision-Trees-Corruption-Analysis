import os
import sys
import functools
import itertools
import random

scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
import dt_algorithm

def calculate_quorum_tree_len(quorum_tree):
    return functools.reduce(lambda count, node: count + len(node), quorum_tree, 0)

def calculate_node_number_of_all_depths_for_quorum_tree(max_depth, quorums):
    return dt_algorithm.calculate_node_number_of_all_depths(max_depth) + (2 * quorums)

def quorum_corruption_validator(node):
    return (sum(node) / len(node)) > 0.5

def build_all_quorum_tree_combinations(max_depth, number_of_quorums):
    size = dt_algorithm.calculate_node_number_of_all_depths(max_depth)
    for positions in itertools.combinations(range(size), number_of_quorums):
        p = [[0] for _ in range(size)]

        for i in positions:
            p[i] = [0, 0, 0]

        yield p

def corrupt_node_for_quorum_tree(quorum_tree, positions):
    size = calculate_quorum_tree_len(quorum_tree)
    currentPosition = 0
    for i, node in enumerate(quorum_tree):
        for j, subnode in enumerate(node):
            if currentPosition in positions:
                quorum_tree[i][j] = 1

            currentPosition += 1

def build_all_corrupted_tree_combinations_for_quorum_tree(quorum_tree, number_of_corrupted_nodes):
    size = calculate_quorum_tree_len(quorum_tree)
    for positions in itertools.combinations(range(size), number_of_corrupted_nodes):

        cp = [x[:] for x in quorum_tree]
        corrupt_node_for_quorum_tree(cp, positions)
        yield cp

def build_all_corrupted_quorum_tree_combinations(max_depth, number_of_quorums, number_of_corrupted_nodes):
    quorum_tree_combinations = build_all_quorum_tree_combinations(max_depth, number_of_quorums)
    for combination in quorum_tree_combinations:
        corrupted_combinations = build_all_corrupted_tree_combinations_for_quorum_tree(combination, number_of_corrupted_nodes)
        for corrupted_combination in corrupted_combinations:
            yield corrupted_combination

def build_random_corrupted_quorum_tree_combinations(max_depth, number_of_quorums, number_of_corrupted_nodes, iterations):
    size = dt_algorithm.calculate_node_number_of_all_depths(max_depth)
    for i in range(iterations):
        p = [[0] for _ in range(size)]

        # Set quorum at random position
        for quorum_position in random.sample(range(size), number_of_quorums):
            p[quorum_position] = [0, 0, 0]

        # Set corrupted nodes at random positions
        overall_size = calculate_node_number_of_all_depths_for_quorum_tree(max_depth, number_of_quorums)
        corrupt_node_for_quorum_tree(p, list(random.sample(range(overall_size), number_of_corrupted_nodes)))
        yield p
