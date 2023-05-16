import json
import os


def count_nodes_recursive(parent_data):
    if parent_data['children'] == [] or parent_data['children'] is None:
        return 0
    counter = len(parent_data["children"])
    for child in parent_data["children"]:
        counter += count_nodes_recursive(child)
    return counter


def count_nodes_in_file(folder_name, file_name):
    path = os.path.join(os.getcwd(), folder_name, file_name)
    with open(path) as read_file:
        json_data = json.load(read_file)
        return count_nodes_recursive(json_data) + 1  # for the root node


def graphs_avg_nodes(folder_path):
    folder = folder_path
    total_nodes = 0
    total_files = 0
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename)) as read_file:
            json_data = json.load(read_file)
        total_nodes += count_nodes_recursive(json_data)
        total_files += 1

    print("Folder name: ", folder_path)
    print("Total nodes: ", total_nodes)
    print("Total files: ", total_files)
    print("Avg nodes: ", total_nodes / total_files)
