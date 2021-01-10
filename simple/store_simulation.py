#!/usr/bin/python3

import os
import sys
import time
import csv
import simulation

scriptpath = "../"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
import dt_algorithm

filename = "../results/simple_simulation.csv"
os.remove(filename) if os.path.exists(filename) else None

csv.register_dialect("semicolon", delimiter=";")
f = open(filename, 'w')
with f:
    writer = csv.writer(f, dialect="semicolon")

    iterations = 100000
    max_depth = 10
    for depth in range(max_depth + 1):

        number_of_nodes = dt_algorithm.calculate_node_number_of_all_depths(depth)
        for corrupted_nodes in range(number_of_nodes):
            print("number of nodes: " + str(number_of_nodes) + " corrupted nodes: " + str(corrupted_nodes))
            start = time.time()
            result = simulation.simulate(depth, corrupted_nodes, iterations)
            end = time.time()
            duration = end - start
            print("duration: " + str(duration))
            dt_algorithm.hr()

            row = [number_of_nodes, corrupted_nodes, result["corruption_factor"], result["success_probability"], duration]
            writer.writerow(row)
