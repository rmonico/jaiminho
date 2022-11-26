#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from argparse import Namespace
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


def main():
    global args

    args = _parse_command_line()

    logger_wrapper.configure(args.verbosity)
    '''
    Logger reference: https://docs.python.org/3/library/logging.html
    '''
    global logger
    logger = logger_wrapper.get(__name__)

    raw_data = _get_raw_request_data(args.request_name)

    request = _build_request(raw_data)

    response = _do_request(request)

    print_response = {}

    print_response['status'] = response['status_code']
    if not response['ok']:
        print_response['headers'] = dict(response['headers'])

    print_response['body'] = response['content']

    import sys
    from pygments import highlight, lexers, formatters

    formatted_json = json.dumps(print_response, ensure_ascii=False, indent=2)

    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalTrueColorFormatter())

    print(colorful_json)


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

    parser.add_argument('request_name', help='Request name')

    logger_wrapper.make_verbosity_argument(parser)

    return parser.parse_args()


def _get_raw_request_data(request_name):
    with open(_request_file(request_name)) as f:
        return yaml.safe_load(f)


def _request_file(request_name):
    global args
    return os.path.join(args.home_folder, request_name + '.yaml')


def _build_request(data: dict):
    request = dict(data['request'])

    namespace_data = _convert_dicts_to_namespace(data)

    request = _format_all_strs_on_dict(namespace_data, request)

    return request


def _convert_dicts_to_namespace(d: dict) -> Namespace:
    for key, value in d.items():
        if type(value) == dict:
            d[key] = Namespace(**_convert_dicts_to_namespace(value))

    return d


def _format_all_strs_on_dict(variables: dict, d: dict) -> dict:
    for key, value in d.items():
        formatted = _format_all_strs(variables, value)

        if formatted != value:
            d[key] = formatted

    return d


def _format_all_strs(variables: dict, obj: object) -> dict:
    if type(obj) == dict:
        return _format_all_strs_on_dict(variables, obj)

    elif type(obj) == list:
        return [ _format_all_strs(variables, item) for item in obj ]

    if type(obj) == str:
        return obj.format(**variables)

    return obj


def _do_request(request):
    with requests.request(**request) as response:
        return {
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


if __name__ == '__main__':
    main()
