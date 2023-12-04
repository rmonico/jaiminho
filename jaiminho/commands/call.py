import os
import yaml
from argparse import Namespace
import requests
import json
from .commons import request_file, environment_file
import logger_wrapper


logger = logger_wrapper.get(__name__)


def run(args_):
    global args
    args = args_

    environment = _load_environment(args.environment, args.request_name)

    raw_data = _get_raw_request_data(args.request_name)

    request = _build_request(raw_data, environment)

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

    if response['status_code']:
        run_on_2xx_rules(raw_data, response['content'])


def _load_environment(environment_name, request_name):
    concrete = dict()

    folders = request_name.split('/')
    for i in range(len(folders)):
        abstract = _get_raw_environment_data(folders[:i])

        if environment_name == '':
            environment_name = abstract.get('selected', '')

        concrete.update(_get_environment(abstract, environment_name))

    return concrete


def _get_raw_environment_data(folders):
    global args

    environmentFile = environment_file(args, folders)

    if not os.path.exists(environmentFile):
        return {}

    with open(environmentFile) as f:
        return yaml.safe_load(f)


def _get_environment(raw, name):
    for environment in raw.get('environments', []):
        if environment.get('name', '') == name:
            return environment

    return {}


def _get_raw_request_data(request_name):
    global args

    with open(request_file(args, request_name)) as f:
        return yaml.safe_load(f)


def _build_request(data: dict, environment: dict) -> dict:
    request = dict(data['request'])

    request = _format_all_strs_on_dict(environment, request)

    return request


def _format_all_strs_on_dict(environment: dict, d: dict) -> dict:
    for key, value in d.items():
        formatted = _format_all_strs(environment, value)

        if formatted != value:
            d[key] = formatted

    return d


def _format_all_strs(environment: dict, obj: object) -> dict:
    if type(obj) == dict:
        return _format_all_strs_on_dict(environment, obj)

    if type(obj) == str:
        # FIXME Cant be this way, use another form of metadata
        if obj.startswith('@'):
            file_path = os.path.join(args.home_folder, obj[1:] + '.data')
            with open(file_path) as f:
                return '\n'.join(f.readlines()).strip()
        else:
            return obj.format(**environment)

    return obj

def _do_request(request):
    logger.debug('Requesting: ' + str(request))

    with requests.request(**request) as response:
        try:
            content = response.json()
        except requests.exceptions.JSONDecodeError:
            content = response.text

        return {
            'apparent_encoding': response.apparent_encoding,
            'content': content,
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


def run_on_2xx_rules(raw_data, response):
    if 'on 2xx' not in raw_data:
        return

    if 'save' not in raw_data['on 2xx']:
        return

    save_data = raw_data['on 2xx']['save']
    filename = save_data['on_file'] + '.data'
    filepath = os.path.join(args.home_folder, filename)
    response_key = save_data['json_key']

    value = response[response_key]

    with open(filepath, 'w') as f:
        f.write(value)

