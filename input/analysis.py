#!/usr/bin/python3

import os
import sys
import getopt
import ast
import input_algorithm

scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
import dt_algorithm

def parse_tree_combination(tree_combinations):
    print(tree_combinations)
    return ast.literal_eval(tree_combinations)

def analyse(tree_combinations, verbose=False):
    tree_combinations_generator = input_algorithm.build_corrupted_tree_combinations
    tree_combinations_generator_params = {"tree_combinations": tree_combinations}
    corruption_factor_calculator = dt_algorithm.calculate_corruption_factor_of_corrupted_parent_nodes
    corruption_factor_calculator_params = {"max_visits": 100}
    corruption_validator = input_algorithm.input_corruption_validator

    paths_generator = dt_algorithm.build_all_paths
    max_depth = len(tree_combinations[0]).bit_length() - 1
    path_generator_params = {"max_depth": max_depth}

    corruption_factor_result = {}
    for corruption_factor in dt_algorithm.analyse_corruption_factors(tree_combinations_generator,
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

    print('tree combinations: ' + str(tree_combinations))
    print("final corruption factor: " + str(corruption_factor_result))
    print("final success probability: " + str(dt_algorithm.calculate_attack_success_probability(corruption_factor_result)))
    return {"corruption_factor": corruption_factor_result, "success_probability": dt_algorithm.calculate_attack_success_probability(corruption_factor_result)}

def main(argv):
    tree_combinations = []
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "ht:v", ["tree_combinations=", "verbose"])
    except getopt.GetoptError:
        print("analysis.py -t <tree combinations> -v <verbose>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("analysis.py -t <tree combinations> -v <verbose>")
            sys.exit()
        elif opt in ("-t", "--tree_combinations"):
            tree_combinations = parse_tree_combination(arg)
        elif opt in ("-v", "--verbose"):
            verbose = True

    print('tree_combinations is ' + str(tree_combinations))
    print('verbose mode is on') if verbose else None
    dt_algorithm.hr()

    # Here is the analysis executed
    analyse(tree_combinations, verbose)

if __name__ == "__main__":
    main(sys.argv[1:])
