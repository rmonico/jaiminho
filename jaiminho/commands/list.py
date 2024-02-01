import os

def run(args):
    _print(args.home_folder, len(args.home_folder) + 1)


def _print(folder_path, base_path_length, indent_level=0):
    with os.scandir(folder_path) as it:
        for entry in it:
            if entry.is_dir():
                _print(os.path.join(folder_path, entry.name), base_path_length, indent_level+1)
            elif _is_request_file(entry):
                _print_request(base_path_length, entry.path)

def _is_request_file(entry: str) -> bool:
    return entry.is_file() and '__environment__' not in entry.name and entry.name.endswith(('.yaml', '.yml'))

def _print_request(base_path_length, request_file_name):
    with open(request_file_name) as request_file:
        import yaml

        request = yaml.safe_load(request_file)

    method = request['request']['method']

    request_name = request_file_name[base_path_length:-5]

    print(f'{method.upper().ljust(7)} {request_name}')
