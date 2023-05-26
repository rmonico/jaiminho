from os import path

# TODO Get global args
def request_file(args, request_name: str) -> str:
    # FIXME Will not work on Windows due to /'s
    return path.join(args.home_folder, request_name + '.yaml') 


def environment_file(args, folders: list) -> str:
    return path.join(args.home_folder, *folders, '__environment__.yaml')

