import random
import itertools
import collections
import functools

def calculate_node_number_of_all_depths(max_depth):
    return 2**(max_depth + 1) - 1

def calculate_node_number_of_depth(depth):
    return 2**depth

def calculate_depth_of_node(node):
    return (node + 1).bit_length() - 1

def calculate_corruption_factor_of_corrupted_parent_nodes(corrupted_parent_nodes, max_visits):
    corruption_factor = 0
    for node in corrupted_parent_nodes:
        node_depth = calculate_depth_of_node(node)
        nodes_for_depth = calculate_node_number_of_depth(node_depth)
        corruption_factor += max_visits / nodes_for_depth
    return corruption_factor

def calculate_attack_success_probability(corruption_factors):
    attack_success_probability = 0
    count = 0
    for key, value in corruption_factors.items():
        if value == 0:
            continue

        count += value
        attack_success_probability += key * value

    return attack_success_probability / count

def build_all_paths(max_depth):

    def build_all_paths_recursive(max_depth, current_depth, offset):
        if (current_depth == max_depth):
            return [[((2**current_depth) - 1) + offset]]

        # left child
        left_offset = 2 * offset + 0
        left_paths = build_all_paths_recursive(max_depth, current_depth + 1, left_offset)

        # right child
        right_offset = 2 * offset + 1
        right_paths = build_all_paths_recursive(max_depth, current_depth + 1, right_offset)

        node = ((2**current_depth) - 1) + offset

        all_path = []
        for path in left_paths:
            path.insert(0, node)
            all_path.append(path)

        for path in right_paths:
            path.insert(0, node)
            all_path.append(path)

        return all_path

    return build_all_paths_recursive(max_depth, 0, 0)

def simulate_corruption_factors(tree_combinations_generator, tree_combinations_generator_params,
                                paths_generator, path_generator_params,
                                corruption_factor_calculator, corruption_factor_calculator_params,
                                corruption_validator, verbose):
    corruption_factors = {}
    paths = list(paths_generator(**path_generator_params))

    if verbose:
        print("all paths: " + str(paths))
        hr()

    for tree in tree_combinations_generator(**tree_combinations_generator_params):
        corrupted_parent_nodes = set()
        for path in paths:
            for node in path:
                if corruption_validator(tree[node]):
                    corrupted_parent_nodes.add(node)
                    break

        # Calculate corruption factor for current corrupted tree combination
        corruption_factor = {corruption_factor_calculator(corrupted_parent_nodes, **corruption_factor_calculator_params): 1}

        # Combine corruptions
        corruption_factors = dict(collections.Counter(corruption_factors) + collections.Counter(corruption_factor))

        if verbose:
            print("tree: " + str(tree))
            print("corrupted parent nodes: " + str(corrupted_parent_nodes) + " corruption factor: " + str(corruption_factor))

        yield corruption_factors

def analyse_corruption_factors(tree_combinations_generator, tree_combinations_generator_params,
                               paths_generator, path_generator_params,
                               corruption_factor_calculator, corruption_factor_calculator_params,
                               corruption_validator, verbose):

    corruption_factors = {}
    paths = list(paths_generator(**path_generator_params))

    if verbose:
        print("all paths: " + str(paths))
        hr()

    for tree in tree_combinations_generator(**tree_combinations_generator_params):
        corrupted_parent_nodes = set()
        for path in paths:
            for node in path:
                if corruption_validator(tree[node]):
                    corrupted_parent_nodes.add(node)
                    break

        # Calculate corruption factor for current corrupted tree combination
        corruption_factor = {corruption_factor_calculator(corrupted_parent_nodes, **corruption_factor_calculator_params): 1}

        # Combine corruptions
        corruption_factors = dict(collections.Counter(corruption_factors) + collections.Counter(corruption_factor))

        if verbose:
            print("tree: " + str(tree))
            print("corrupted parent nodes: " + str(corrupted_parent_nodes) + " corruption factor: " + str(corruption_factor))

        yield corruption_factors

def hr():
    print("-" * 100)
