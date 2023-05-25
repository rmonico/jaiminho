import os

def run(args):
    _print(args.home_folder, len(args.home_folder) + 1)


def _print(folder_path, base_path_length, indent_level=0):
    with os.scandir(folder_path) as it:
        for entry in it:
            if entry.is_dir():
                _print(os.path.join(folder_path, entry.name), base_path_length, indent_level+1)
            elif entry.is_file() and entry.name.endswith(('.yaml', '.yml')):
                print(entry.path[base_path_length:-5])

