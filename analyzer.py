import json
import os
import matplotlib.pyplot as plt
from time import sleep
import numpy as np
import itertools


time = ["15","60"]
mbps = ["1Mbps","2Mbps","3Mbps", "4Mbps", "5Mbps"]

def visualize_data(event_counts, t, m):
    # Extract the keys and values from the dictionary
    events = list(event_counts.keys())
    counts = list(event_counts.values())

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 8))
    y_positions = range(len(events))  # The bar positions on the y-axis

    plt.barh(y_positions, counts, color='skyblue')
    plt.yticks(y_positions, events)  # Set the y-ticks to show event names
    plt.xlabel('Labels')
    plt.title(f'QoS of {t} seconds at {m}')

    # Add the data labels to each bar
    for i, count in enumerate(counts):
        plt.text(count, i, str(count), va='center')

    # Adjust layout to make room for the labels
    plt.tight_layout()
    
    # Show the plot
    plt.show()

def tally_events_in_folder(folder_path, current_data):
    event_tally = current_data  # Dictionary to hold the tally of each event

    # Step 1: List all files in the given folder
    for filename in os.listdir(folder_path):
        # Check if the file is a JSON file
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)

            # Step 2: Load the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Assuming the data structure is a list of dictionaries at the root
            # Step 3: Tally the occurrences of each event
            for request in data:
                # Assuming each request has a "method" key or change "method" to your specific key
                if "method" in request:
                    method = request["method"]
                    if method in event_tally:
                        event_tally[method] += 1
                    else:
                        event_tally[method] = 1

    # Step 4: Display the tally
    return event_tally

def ten_graph_visualize_data(folder_path, time, mbps):
    fig, axes = plt.subplots(len(time), len(mbps), figsize=(20, 15), squeeze=False)

    for i, t in enumerate(time):
        for j, m in enumerate(mbps):
            current_data = {}
            for s in range(1, 6):
                directory = f"{folder_path}/{s}/{t}/{m}/QoS"
                current_data = tally_events_in_folder(directory, current_data)
            events = list(current_data.keys())
            counts = list(current_data.values())
            ax = axes[i][j]  # Select the correct subplot
            y_positions = range(len(events))

            ax.barh(y_positions, counts, color='skyblue')
            ax.set_yticks(y_positions)
            ax.set_yticklabels(events)
            ax.set_xlabel('Count')
            ax.set_title(f'QoS of {t} seconds at {m}')

            # Add the data labels to each bar
            for y_pos, count in zip(y_positions, counts):
                ax.text(count, y_pos, str(count), va='center')
            print(f"Something happened i:{i} j:{j}")

    plt.tight_layout()
    plt.show()

def one_graph_visualize_data(root_folder_path, time, mbps):
    # More color options
    colors = plt.cm.tab20.colors  # This will give you 20 color options
    
    # Calculate the total number of unique methods across all files for setting x_ticks later
    unique_methods = set()
    for t, m in itertools.product(time, mbps):
        folder_path = os.path.join(root_folder_path, f"1/{t}/{m}/QoS")
        unique_methods.update(tally_events_in_folder(folder_path, {}).keys())
    unique_methods = sorted(unique_methods)  # Sort to keep consistency

    fig, ax = plt.subplots(figsize=(15, 10))
    width = 0.1  # Width of the bar
    # The offset distance between different categories
    offset = width * 1.5  

    # Initialize a counter for the x-axis positions
    base_x_positions = np.arange(len(unique_methods))
    
    for i, (t, m) in enumerate(itertools.product(time, mbps)):
        # Construct the folder path for each condition
        current_data = {}
        for s in range(1, 6):
            directory = f"tiktok_data/{s}/{t}/{m}/QoS"
            current_data = tally_events_in_folder(directory, current_data)
        
        # Create a list of counts for each unique method, ensuring they are in the correct order
        counts = [current_data.get(method, 0) for method in unique_methods]
        
        # Calculate positions for the groups of bars
        positions = [x + (i * offset) for x in base_x_positions]

        ax.bar(positions, counts, width=width, color=colors[i % len(colors)], label=f'{t}s at {m}')
        print(f"Success for run:{i}")

    # Set the x-ticks to be in the middle of the groups
    tick_positions = [x + (offset * ((len(time) * len(mbps) - 1) / 2)) for x in base_x_positions]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(unique_methods, rotation=45, ha='right')
    ax.set_ylabel('Count')
    ax.set_ylim(0, 400000)
    ax.set_title('Combined QoS Graph')
    ax.legend()

    plt.tight_layout()
    plt.show()

# Example usage
# for t in time:
#     for m in mbps:
#         current_data = {}
#         for s in range(1, 6):
#             directory = f"tiktok_data/{s}/{t}/{m}/QoS"
#             current_data = tally_events_in_folder(directory, current_data)
#         visualize_data(current_data, t, m)

# one_graph_visualize_data("tiktok_data", time, mbps)
    
root_folder_path = 'tiktok_data'  # replace with your actual path
time = [["15"],["60"]]
mbps_set = ["1Mbps", "2Mbps", "3Mbps", "4Mbps", "5Mbps"]  # Split the mbps categories into two sets

for t in time:
    one_graph_visualize_data(root_folder_path, t, mbps_set)


