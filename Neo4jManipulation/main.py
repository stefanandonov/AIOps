import os
from service import get_processed_files_hash, file_to_db, delete_all_from_db
from statistics import count_nodes_in_file, graphs_avg_nodes

if __name__ == "__main__":
    #delete_all_from_db()
    # STATISTICS:
    # for folder_path in ["../concurrent data/concurrent data/traces/boot_delete", "path2", "..pathN"]:
    #      graphs_avg_nodes(folder_path)


    path = "../concurrent data/concurrent data/traces/network_create_delete"
    folder_name = "network_create_delete"
    processed_files = get_processed_files_hash()
    print(processed_files)
    for file_name in os.listdir(path):
        file_folder_name = file_name+folder_name
        if file_folder_name not in processed_files:
            print("Starting to process file:", file_name)
            print("Nodes in file: ", count_nodes_in_file(path,file_name))
            file_to_db(path, folder_name, file_name)
            print("Finished processing file:", file_name)
