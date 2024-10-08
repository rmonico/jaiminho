#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logger_wrapper

import os
import sys

from .commands import list as list_command, call as call_command, edit as edit_command, new as new_command, remove as remove_command, view as view_command, export_curl as export_curl_command


HOME_FOLDER_VARIABLE = 'JAIMINHO'
DEFAULT_HOME_FOLDER = '{HOME}/.config/jaiminho'.format(**os.environ)


def main():
    global args

    parser, args = _parse_command_line()

    logger_wrapper.configure(args.verbosity)
    '''
    Logger reference: https://docs.python.org/3/library/logging.html
    '''
    global logger
    logger = logger_wrapper.get(__name__)

    if not hasattr(args, 'command'):
        parser.print_help()
        return 0

    return args.command.run(args)


def var_list(raw):
    key_values = raw.split(',')

    result = dict()

    for key_value in key_values:
        key, value = key_value.split('=')

        result[key] = value

    return result


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

    subparsers = parser.add_subparsers()

    call_parser = subparsers.add_parser('request', aliases='r', help='Make a request')
    call_parser.set_defaults(command = call_command)

    call_parser.add_argument('request_name', help='Request name')
    call_parser.add_argument('--environment', '-e', default='', help='Environment to use')
    call_parser.add_argument('--variables', '-v', type=var_list, default=[], help='Variables list, ex: "a=b,c=3"')


    list_parser = subparsers.add_parser('list', aliases=['ls', 'l'], help='List existing requests')
    list_parser.add_argument('--asterisk-glob', '-ag', action='store_true', help='Filter request names by a glob expression, appended with a * (the default)')
    list_parser.add_argument('--glob', '-g', action='store_true', help='Filter request names by a glob expression')
    list_parser.add_argument('--regex', '-r', action='store_true', help='Filter request names by a regex expression')
    list_parser.add_argument('expression', nargs='*', default='*', help='Expression applied to request names')
    list_parser.set_defaults(command = list_command)


    edit_parser = subparsers.add_parser('edit', aliases = ['ed', 'e'] , help='Edit a existing request')
    edit_parser.set_defaults(command = edit_command)

    edit_parser.add_argument('request_name', help='Request to edit')


    new_parser = subparsers.add_parser('new', aliases = ['n'] , help='Create a new request')
    new_parser.add_argument('model', help='Request to use as model')
    new_parser.add_argument('name', help='New request name')
    new_parser.add_argument('--no-edit', '-ne', action='store_true', help='Dont edit request after create it')
    new_parser.set_defaults(command = new_command)


    remove_parser = subparsers.add_parser('remove', aliases=['rm'], help='Remove one or more requests')
    remove_parser.add_argument('request_names', nargs='+', help='Requests to remove')
    remove_parser.set_defaults(command = remove_command)


    view_parser = subparsers.add_parser('view', aliases=['v'], help='View one or more requests')
    view_parser.add_argument('request_names', nargs='+', help='Requests to view')
    view_parser.set_defaults(command = view_command)


    export_parser = subparsers.add_parser('export', help='Export one or more requests')
    export_subparsers = export_parser.add_subparsers()

    export_curl_parser = export_subparsers.add_parser('curl', help='Export requests as curl')
    export_curl_parser.add_argument('request_names', nargs='+', help='Requests to export')
    export_curl_parser.add_argument('--environment', '-e', default='', help='Environment to use')
    export_curl_parser.add_argument('--variables', '-v', type=var_list, default=[], help='Variables list, ex: "a=b,c=3"')
    export_curl_parser.set_defaults(command = export_curl_command)


    logger_wrapper.make_verbosity_argument(parser)

    return parser, parser.parse_args()


if __name__ == '__main__':
    result = main()

    sys.exit(result)

