#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logger_wrapper
import requests
# Disable warning due to certificate
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import yaml
import os
import json

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

    parser.add_argument('--dry-run',
                        help='Show arguments being used, actually do nothing')

    parser.add_argument('request_name', help='Request name')

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


def _do_request(request):
    with requests.request(**request) as response:
        _response = {
            'apparent_encoding': response.apparent_encoding,
            'content': response.json(),
            # TODO 'cookies': response.cookies,
            'elapsed': str(response.elapsed),
            'encoding': response.encoding,
            'headers': dict(response.headers),
            'history': response.history,
            'is_permanent_redirect': response.is_permanent_redirect,
            'is_redirect': response.is_redirect,
            'links': response.links,
            'next': response.next,
            'ok': response.ok,
            # TODO Ver se tem alguma coisa relevante aqui 'raw': response.raw,
            'reason': response.reason,
            'status_code': response.status_code,
            'url': response.url,
        }

        return _response


def persist(request_name, request, response):
    from datetime import datetime

    registry = {
        'timestamp': datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'request_name': request_name,
        'request': request,
        'response': response,
    }

    database_file_name = os.path.join(args.home_folder, 'history.db')

    from tinydb import TinyDB, Query

    db = TinyDB(database_file_name)

    db.insert(registry)


def main():
    global args

    args = _parse_command_line()

    logger_wrapper.configure(args.verbosity)
    '''
    Logger reference: https://docs.python.org/3/library/logging.html
    '''
    global logger
    logger = logger_wrapper.get(__name__)

    request = _get_request_arguments(args.request_name)

    if args.dry_run:
        print(json.dumps(request))
        return

    response = _do_request(request)

    print_response = {}

    print_response['status'] = response['status_code']
    if not response['ok']:
        print_response['headers'] = dict(response['headers'])

    print_response['body'] = response['content']

    print(json.dumps(print_response))

    persist(args.request_name, request, response)


if __name__ == '__main__':
    main()
