import os
from collections import deque, namedtuple

'''
ToDo:
- Flags:
    -start_path                                 optional start_path different of script path
    -help                                       help
    -abs_path                                   signals that we print the absolute path, not the one relative to the starting path
    -flat                                       signals we only care about data in this directory, ignoring children
    -regex S*[ome]Python-(Regex){3} f/t         include only files which names match the regex (if t) or which don't match the regex (f)
    -custom categoryName .extensionA .extB...   add a custom category with files to parse which have any of the specified extensions 
'''

flag_abs_path = False
flag_flat = False

DirData = namedtuple("DirData", "file_name_list dir_path_list")

# category -> list of urls
parsed_data = dict()


def analyze_dir(path):
    # print(path)
    files_and_dirs = os.listdir(path)
    file_names, dir_paths = [], []
    for entry in files_and_dirs:
        # print("?: " + path + os.path.sep + entry)
        if os.path.isfile(path + os.path.sep + entry):
            # print("file: " + os.path.basename(entry))
            file_names.append(os.path.basename(entry))
        else:
            # print("dir: " + path + os.path.sep + entry)
            dir_paths.append(path + os.path.sep + entry)
    return DirData(file_names, dir_paths)


def do_the_thing(start_dir=os.path.dirname(os.path.abspath(__file__))):
    dir_dict = {}
    file_dict = {}
    start_dir = os.path.normpath(os.path.normcase(start_dir))
    # ToDo add option for user input path
    # deque with absolute path of the file
    dir_deque = deque()
    dir_deque.append(start_dir)

    # iterate through all directories and save discovered files and directories in dir_dict
    while dir_deque:
        curr_dir = dir_deque.popleft()
        dir_dict[curr_dir] = analyze_dir(curr_dir)
        # only recurse if we aren't searching flat
        if not flag_flat:
            for dir_name in dir_dict[curr_dir].dir_path_list:
                dir_deque.append(dir_name)

    extension_dict = dict()
    for dir_url, dir_data in dir_dict.items():
        for file_name in dir_data.file_name_list:
            _, extension = os.path.splitext(file_name)
            if extension:
                wanted_path = dir_url + os.path.sep + file_name if flag_abs_path else os.path.relpath(
                    dir_url + os.path.sep + file_name)
                if extension not in extension_dict:
                    extension_dict[extension] = [wanted_path]
                else:
                    extension_dict[extension].append(wanted_path)

    return extension_dict

print(do_the_thing())