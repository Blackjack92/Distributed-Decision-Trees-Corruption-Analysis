#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

csv_file = "../results_analysis/simulation.csv"

headers = ["node count", "corrupted count", "corruption factor", "attack success", "duration"]
data = pd.read_csv(csv_file, sep=";", names=headers)

# Filter by node count
data_1nodes = data[data["node count"] == 1]
data_3nodes = data[data["node count"] == 3]
data_7nodes = data[data["node count"] == 7]
data_15nodes = data[data["node count"] == 15]
data_31nodes = data[data["node count"] == 31]
data_63nodes = data[data["node count"] == 63]
data_127nodes = data[data["node count"] == 127]
data_255nodes = data[data["node count"] == 255]
data_511nodes = data[data["node count"] == 511]
data_1023nodes = data[data["node count"] == 1023]
data_2047nodes = data[data["node count"] == 2047]

plt.plot(data_1nodes["corrupted count"], data_1nodes["attack success"], color="blue")
plt.plot(data_3nodes["corrupted count"], data_3nodes["attack success"], color="red")
plt.plot(data_7nodes["corrupted count"], data_7nodes["attack success"], color="green")
plt.plot(data_15nodes["corrupted count"], data_15nodes["attack success"], color="gray")
plt.plot(data_31nodes["corrupted count"], data_31nodes["attack success"], color="black")
plt.plot(data_63nodes["corrupted count"], data_63nodes["attack success"], color="black")
plt.plot(data_127nodes["corrupted count"], data_127nodes["attack success"], color="black")
plt.plot(data_255nodes["corrupted count"], data_255nodes["attack success"], color="black")
plt.plot(data_511nodes["corrupted count"], data_511nodes["attack success"], color="black")
plt.plot(data_1023nodes["corrupted count"], data_1023nodes["attack success"], color="black")
plt.plot(data_2047nodes["corrupted count"], data_2047nodes["attack success"], color="black")

plt.plot(data_2047nodes["corrupted count"], [50] * len(data_2047nodes["corrupted count"]), color="black", linestyle="--")

plt.show()
