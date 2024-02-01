from jaiminho.commands.commons import request_file
import os


def run(args):
    some_request_not_found = False

    for request_name in args.request_names:
        request_path = request_file(args, request_name)

        if os.path.exists(request_path):
            os.unlink(request_path)
            print(f'Request "{request_name}" removed')
        else:
            print(f'Request "{request_name}" not found')
            some_request_not_found = True


    return 1 if some_request_not_found else 0

