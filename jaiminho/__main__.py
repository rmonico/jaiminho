#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logger_wrapper
# Disable warning due to certificate
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import yaml
import os
import sys

from .commands import list as list_command, call as call_command, edit as edit_command, new as new_command


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

    return args.command.run(args)


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

    call_parser = subparsers.add_parser('call', aliases='c', help='Make a request')
    call_parser.set_defaults(command = call_command)

    call_parser.add_argument('request_name', help='Request name')
    call_parser.add_argument('--environment', '-e', default='', help='Request name')


    list_parser = subparsers.add_parser('list', aliases = ['ls', 'l'] , help='List existing requests')
    list_parser.set_defaults(command = list_command)


    edit_parser = subparsers.add_parser('edit', aliases = ['ed', 'e'] , help='Edit a existing request')
    edit_parser.set_defaults(command = edit_command)

    edit_parser.add_argument('request_name', help='Request to edit')


    new_parser = subparsers.add_parser('new', aliases = ['n'] , help='Create a new request')
    new_parser.set_defaults(command = new_command)

    new_parser.add_argument('name', help='New request name')
    new_parser.add_argument('--model', '-m', help='Request to use as model')


    logger_wrapper.make_verbosity_argument(parser)

    return parser.parse_args()


if __name__ == '__main__':
    result = main()

    sys.exit(result)

