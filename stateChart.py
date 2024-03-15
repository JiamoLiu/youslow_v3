import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from collections import OrderedDict

time = ["15", "60"]
mbps = ["1Mbps", "2Mbps", "3Mbps", "4Mbps", "5Mbps"]
runs = range(1, 6)  # Assuming runs from 1 to 5
colors = ['red', 'blue', 'green', 'orange', 'purple']  # Different colors for each network state

def chart_state_all_conditions():
    fig, axes = plt.subplots(len(time), len(mbps), figsize=(20, 10), sharey=True)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)

    for i, t in enumerate(time):
        for j, m in enumerate(mbps):
            state_counts = {s: {state: 0 for state in range(5)} for s in runs}  # Now includes states 0-4
            
            for s in runs:
                directory = f'tiktok_data/{s}/{t}/{m}/QoE'
                for filename in os.listdir(directory):
                    if filename.endswith(".csv"):
                        filepath = os.path.join(directory, filename)
                        df = pd.read_csv(filepath)
                        states = df['networkState']
                        for state in states:
                            state_counts[s][state] += 1  # Direct tally without checking existence

            # Plotting with offset for each state to avoid overlap
            offset = 0.1  # Small offset for each state
            for s in runs:
                labels_plotted = []  # Keep track of which labels have been plotted
                for state in range(5):  # Explicitly iterate through states 0-4
                    count = state_counts[s][state]
                    bar_position = s + (state - 2) * offset  # Adjust position for 5 states
                    label = f'State {state}' if state not in labels_plotted else None
                    axes[i, j].bar(bar_position, count, width=offset, color=colors[state % len(colors)], label=label)
                    if label: labels_plotted.append(state)
            
            axes[i, j].set_title(f'{t}s at {m}')
            axes[i, j].set_xlabel('Run')
            axes[i, j].set_ylabel('Frequency')
            axes[i, j].set_xticks(runs)

    # Create a legend for the states in order
    handles, labels = [], []
    for state in range(5):  # Adjust for states 0-4
        handles.append(plt.Rectangle((0,0),1,1, color=colors[state % len(colors)]))
        labels.append(f'State {state}')

    fig.legend(handles, labels, loc='upper right')

    plt.show()


chart_state_all_conditions()
