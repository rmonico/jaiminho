import os
import requests
import json
from .commons import create_request
import logger_wrapper


logger = logger_wrapper.get(__name__)


def run(args_):
    global args
    args = args_

    request, raw_data = create_request(args.home_folder, args.environment, args.request_name, args.variables)

    response = _do_request(request)

    print_response = {}

    print_response['status'] = response['status_code']
    if not response['ok']:
        print_response['headers'] = dict(response['headers'])

    print_response['body'] = response['content']

    from pygments import highlight, lexers, formatters

    formatted_json = json.dumps(print_response, ensure_ascii=False, indent=2)

    colorful_json = highlight(formatted_json, lexers.JsonLexer(),
                              formatters.TerminalTrueColorFormatter())

    print(colorful_json)

    if response['status_code'] in range(200, 300):
        run_on_2xx_rules(raw_data, response['content'])
    else:
        logger.warn('Skipped 2xx rules, non-ok status returned')


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
