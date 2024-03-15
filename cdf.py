import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from time import sleep

time = ["15","60"]
mbps = ["1Mbps","2Mbps","3Mbps", "4Mbps", "5Mbps"]

def extract_final_values(directory):
    final_values = []
    
    # Iterate through all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(filepath)
            # Extract the final value of the "webkitDecodedFrameCount" column
            final_value = df['networkState'].iloc[-1]
            final_values.append(final_value)
    
    return final_values

def plot_cdf(final_values, t, m):
    sorted_values = np.sort(final_values)
    yvals = np.arange(len(sorted_values)) / float(len(sorted_values))
    plt.plot(sorted_values, yvals)
    plt.xlabel('Final Webkit Dropped Frame Count')
    plt.ylabel('CDF')
    plt.title(f'CDF of Webkit Dropped Frame Count for {t} seconds at {m}')
    plt.grid(True)
    plt.show()

def chart_state(directory, t, m, s):
    state_counts = {}
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            states = df['networkState']
            for state in states:
                if state not in state_counts:
                    state_counts[state] = 1
                else:
                    state_counts[state] += 1
    states = list(state_counts.keys())
    counts = list(state_counts.values())
    
    plt.figure(figsize=(10, 6))
    plt.bar(states, counts, color='skyblue')
    plt.xlabel('Network State')
    plt.ylabel('Frequency')
    plt.title(f'Run {s}: Frequency of Network States for {t} seconds at {m}')
    plt.xticks(states)
    plt.grid(axis='y')
    plt.show()


# Example usage
    

for t in time:
    for m in mbps:
        final_values = []
        for s in range(1,6):
            directory = f'tiktok_data/{s}/{t}/{m}/QoE'
            chart_state(directory, t, m, s)