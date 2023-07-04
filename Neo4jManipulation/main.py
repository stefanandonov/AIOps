import os
from service import get_processed_files_hash, file_to_db
from statistics import count_nodes_in_file, graphs_avg_nodes

if __name__ == "__main__":
    # STATISTICS:
    for folder_path in ["../concurrent data/concurrent data/traces/boot_delete", "path2", "..pathN"]:
         graphs_avg_nodes(folder_path)


    folder_name = "../concurrent data/concurrent data/traces/boot_delete"
    processed_files = get_processed_files_hash()
    for file_name in os.listdir(folder_name):
        if file_name not in processed_files:
            print("Starting to process file:", file_name)
            print("Nodes in file: ", count_nodes_in_file(folder_name,file_name))
            file_to_db(folder_name, file_name)
            print("Finished processing file:", file_name)
