import os
import sys
import itertools
import random

scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
import dt_algorithm

def input_corruption_validator(node):
    return (sum(node) / len(node)) > 0.5

def build_corrupted_tree_combinations(tree_combinations):
    for tree_combination in tree_combinations:
        yield tree_combination
