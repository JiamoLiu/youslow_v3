
import os
import json

def add_line_breaks(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)

    json_string = json.dumps(data, indent=4)
    json_string_with_line_breaks = json_string.replace(',{"method"', '\n,{"method"')
    return json_string_with_line_breaks

def remove_extra_newlines(input_file, output_file):
    with open(input_file, 'r') as file:
        # Read the JSON file
        lines = file.readlines()
    cleaned_lines = []
    for line in lines:
        if line.strip():  # Ignore empty lines
            cleaned_lines.append(line.rstrip())
    cleaned_content = '\n'.join(cleaned_lines)
    data = json.loads(cleaned_content)
    formatted_json_str = json.dumps(data, indent=4)
    with open(output_file, 'w') as file:
        file.write(formatted_json_str)


folder_paths = ["dataset/15/campus/4Mbps"]


for folder_path in folder_paths:
    for i in range(1, 3):
        qos_folder = os.path.join(folder_path, str(i), "QoS")
        for file_name in os.listdir(qos_folder):
            if file_name.endswith(".json"):
                json_file = os.path.join(qos_folder, file_name)
                json_string_with_line_breaks = add_line_breaks(json_file)
                with open(json_file, 'w') as file:
                    file.write(json_string_with_line_breaks)

