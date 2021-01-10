#!/usr/bin/python3

import os
import sys
import time
import csv
import analysis
import quorum_algorithm

scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
import dt_algorithm

filename = "../results/quorum_analysis.csv"
os.remove(filename) if os.path.exists(filename) else None

csv.register_dialect("semicolon", delimiter=";")
f = open(filename, 'w')
with f:
    writer = csv.writer(f, dialect="semicolon")

    max_depth = 4
    for depth in range(max_depth + 1):

        number_of_nodes = dt_algorithm.calculate_node_number_of_all_depths(depth)
        for number_of_quorums in range(number_of_nodes):
            number_of_inner_nodes = quorum_algorithm.calculate_node_number_of_all_depths_for_quorum_tree(depth, number_of_quorums)

            for corrupted_nodes in range(number_of_inner_nodes):
                print("number of nodes: " + str(number_of_nodes) + " number of quorums: " + str(number_of_quorums))
                print("number of inner nodes: " + str(number_of_inner_nodes) + " corrupted nodes: " + str(corrupted_nodes))

                start = time.time()
                result = analysis.analyse(depth, number_of_quorums, corrupted_nodes)
                end = time.time()

                duration = end - start
                print("duration: " + str(duration))
                dt_algorithm.hr()

                row = [number_of_nodes, number_of_quorums, number_of_inner_nodes, corrupted_nodes, result["corruption_factor"], result["success_probability"], duration]
                writer.writerow(row)
