from jaiminho.commands.commons import request_file, create_request
import os


def run(args):
    some_request_not_found = False

    for request_name in args.request_names:
        request_path = request_file(args.home_folder, request_name)

        if os.path.exists(request_path):
            request, raw_data = create_request(args.home_folder, args.environment, request_name)

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
    return f" --data '{data}'"
