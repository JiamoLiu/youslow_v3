import json
import os

time = ["15","60"]
mbps = ["1Mbps","2Mbps","3Mbps", "4Mbps", "5Mbps"]


def adjustJSON(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                json_data = file.read()
                parts = json_data.split(', {"m')
                formatted_json = ',\n{"m'.join(parts)
                with open(file_path, 'w') as file:
                    file.write(formatted_json)



for t in time:
    for m in mbps:
        for s in range(1,6):
            directory = f'tiktok_data/{s}/{t}/{m}/QoS'
            adjustJSON(directory)

# adjustJSON(f'tiktok_data/test')