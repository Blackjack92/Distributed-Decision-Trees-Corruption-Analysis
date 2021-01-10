#!/usr/bin/python3

import os
import sys
import getopt
import quorum_algorithm

scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
import dt_algorithm


def simulate(max_depth, number_of_quorums, number_of_corrupted_nodes, iterations, verbose=False):
    tree_combinations_generator = quorum_algorithm.build_random_corrupted_quorum_tree_combinations
    tree_combinations_generator_params = {"max_depth": max_depth, "number_of_quorums": number_of_quorums,
                                          "number_of_corrupted_nodes": number_of_corrupted_nodes, "iterations": iterations}
    corruption_factor_calculator = dt_algorithm.calculate_corruption_factor_of_corrupted_parent_nodes
    corruption_factor_calculator_params = {"max_visits": 100}
    corruption_validator = quorum_algorithm.quorum_corruption_validator

    paths_generator = dt_algorithm.build_all_paths
    path_generator_params = {"max_depth": max_depth}

    corruption_factor_result = {}
    for corruption_factor in dt_algorithm.simulate_corruption_factors(tree_combinations_generator,
                                                                      tree_combinations_generator_params,
                                                                      paths_generator,
                                                                      path_generator_params,
                                                                      corruption_factor_calculator,
                                                                      corruption_factor_calculator_params,
                                                                      corruption_validator,
                                                                      verbose):

        corruption_factor_result = corruption_factor
        if verbose:
            print("intermediate corruption factors: " + str(corruption_factor))
            print("intermediate success probability: " + str(dt_algorithm.calculate_attack_success_probability(corruption_factor)))
            dt_algorithm.hr()

    print('max tree depth: ' + str(max_depth) + ' number of nodes: ' + str(dt_algorithm.calculate_node_number_of_all_depths(max_depth)))
    print('number of quorums: ' + str(number_of_quorums))
    print('number of corrupted nodes: ' + str(number_of_corrupted_nodes))
    print("final corruption factors: " + str(corruption_factor_result))
    print("final success probability: " + str(dt_algorithm.calculate_attack_success_probability(corruption_factor_result)))
    return {"corruption_factor": corruption_factor_result, "success_probability": dt_algorithm.calculate_attack_success_probability(corruption_factor_result)}


def main(argv):
    max_depth = 1
    number_of_quorums = 0
    number_of_corrupted_nodes = 0
    iterations = 10000
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hd:q:c:i:v", ["max_depth=", "quorums=", "corrupted_nodes=", "iterations=", "verbose"])
    except getopt.GetoptError:
        print("analysis.py -d <max tree depth> -q <number of quorums> -c <number of corrupted nodes> -i <iterations> -v <verbose>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("analysis.py -d <max tree depth> -q <number of quorums> -c <number of corrupted nodes> -i <iterations> -v <verbose>")
            sys.exit()
        elif opt in ("-d", "--max_depth"):
            max_depth = int(arg)
        elif opt in ("-q", "--quorums"):
            number_of_quorums = int(arg)
        elif opt in ("-c", "--corrupted_nodes"):
            number_of_corrupted_nodes = int(arg)
        elif opt in ("-i", "--iterations"):
            iterations = int(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True

    print('max_depth is ' + str(max_depth))
    print('number_of_quorums is ' + str(number_of_quorums))
    print('number_of_corrupted_nodes is ' + str(number_of_corrupted_nodes))
    print('iterations is ' + str(iterations))
    print('verbose mode is on') if verbose else None
    dt_algorithm.hr()

    # Here is the analysis executed
    simulate(max_depth, number_of_quorums,
             number_of_corrupted_nodes, iterations, verbose)


if __name__ == "__main__":
    main(sys.argv[1:])
