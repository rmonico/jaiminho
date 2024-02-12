from jaiminho.commands.commons import request_file
import os


def run(args):
    some_request_not_found = False

    for request_name in args.request_names:
        request_path = request_file(args.home_folder, request_name)

        if os.path.exists(request_path):
            # TODO Load variable values! Reuse _load_environment
            # _get_raw_request_data and _build_request from call.py
            with open(request_path) as file:
                import yaml

                raw = yaml.safe_load(file)

            request = raw['request']

            command = 'curl -X {method} {url}'.format(**request)

            if 'headers' in request:
                command += _headers(request['headers'])

            if 'data' in request:
                command += _data(request['data'])

            # TODO Escape for bash
            print(command)
        else:
            print(f'Request "{request_name}" not found')
            some_request_not_found = True

    return 1 if some_request_not_found else 0


def _headers(headers_):
    headers = ''

    for header, value in headers_.items():
        headers += f" -H '{header}: {value}'"

    return headers


def _data(data):
    return f"--data '{data}'"
