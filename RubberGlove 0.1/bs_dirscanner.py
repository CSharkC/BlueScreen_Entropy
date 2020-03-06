import os

def get_file_list(path):
    """Takes a path and returns all the files in and below the path"""
    file_list = [] # list to be populated with all the files
    if os.path.isdir(path):
        for root, _, files in os.walk(f"{path}"):
            for name in files: # itterates over all the files
                file_list.append(os.path.join(root, name)) # itterates over all the files
    elif os.path.isfile(path):
        file_list.append(path)
    else:
        raise PathError
    return file_list
