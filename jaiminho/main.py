#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logger_wrapper
import requests
import yaml
import os

# Disable breakpoints
# breakpoint = lambda: False

HOME_FOLDER_VARIABLE = 'JAIMINHO'
DEFAULT_HOME_FOLDER = '{HOME}/.config/jaiminho'.format(**os.environ)
REQUEST_NAMESPACE_SEPARATOR = '/'
NAMESPACE_DEFAULT_REQUEST = '__default__'


def _parse_command_line():
    '''
    Reference: https://docs.python.org/3/library/argparse.html
    '''
    parser = argparse.ArgumentParser(
        description='Um Postman que evita a fadiga')

    parser.add_argument('--home-folder',
                        default=os.environ.get(HOME_FOLDER_VARIABLE,
                                               DEFAULT_HOME_FOLDER),
                        help='Set alternate home folder')

    parser.add_argument('request', help='Request name')

    logger_wrapper.make_verbosity_argument(parser)

    return parser.parse_args()


def _error(message, exit_code=1):
    global logger
    logger.critical(message)
    sys.exit(exit_code)


def _request_file(request_name):
    global args
    return os.path.join(args.home_folder, request_name + '.yaml')


def _namespace(request_name):
    last_separator = request_name.rfind(REQUEST_NAMESPACE_SEPARATOR)

    if last_separator > -1:
        return request_name[:last_separator]
    else:
        return None


def _get_request_arguments(request_name):
    breakpoint()
    arguments = list()
    with open(_request_file(request_name)) as f:
        arguments.append(yaml.safe_load(f))

    namespace = request_name
    while namespace := _namespace(namespace):
        namespace_default = namespace + REQUEST_NAMESPACE_SEPARATOR + NAMESPACE_DEFAULT_REQUEST
        with open(_request_file(namespace_default)) as f:
            arguments.append(yaml.safe_load(f))

    arguments.reverse()

    definitive = _make_extensions(arguments)

    return definitive


def _make_extension(subargs, superargs):
    for key, value in superargs.items():
        if key not in subargs:
            subargs[key] = value
        elif isinstance(value, dict):
            _make_extension(subargs[key], value)
        else:
            subargs[key] = value


def _make_extensions(arguments):
    subargs = dict()

    for superargs in arguments:
        _make_extension(subargs, superargs)

    return subargs


def _do_request(args):
    request_arguments = _get_request_arguments(args.request)

    print(request_arguments)


#     with requests.request(**args) as r:
#         return r


def main():
    global args

    args = _parse_command_line()

    logger_wrapper.configure(args.verbosity)
    '''
    Logger reference: https://docs.python.org/3/library/logging.html
    '''
    global logger
    logger = logger_wrapper.get(__name__)

    # breakpoint()
    response = _do_request(args)

    # print(response.json())
    # print(response.headers)


if __name__ == '__main__':
    main()
