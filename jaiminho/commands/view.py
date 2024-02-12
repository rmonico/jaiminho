from jaiminho.commands.commons import request_file
import os


def run(args):
    some_request_not_found = False

    separator = '------'

    for i, request_name in enumerate(args.request_names):
        request_path = request_file(args.home_folder, request_name)

        if os.path.exists(request_path):
            with open(request_path) as file:
                for line in file.readlines():
                    print(line.rstrip())
        else:
            print(f'Request "{request_name}" not found')
            some_request_not_found = True

        if i < len(args.request_names) - 1:
            print()
            print(separator)
            print()

    return 1 if some_request_not_found else 0

