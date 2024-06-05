import fnmatch
import logger
import os
import re


log = logger.get(__name__)


FILTERS = [
        lambda expression: AsteriskGlobFilter(expression),
        lambda expression: GlobFilter(expression),
        lambda expression: RegexFilter(expression)]


def run(args):
    command = ListCommand(
            args.home_folder,
            args.asterisk_glob,
            args.glob,
            args.regex,
            ' '.join(args.expression))
    command.run()


class ListCommand(object):

    def __init__(self, folder_path, asterisk_glob, glob, regex, expression):
        log.info(f'Listing with: path {folder_path}, expression: {expression}, asteriskglob: {asterisk_glob}, glob: {glob}, regex: {regex}')
        self._folder_path = folder_path
        self._filter = self._get_filter(expression, asterisk_glob, glob, regex)
        self._base_path_length = len(folder_path) + 1

    @staticmethod
    def _get_filter(expression, *_flags):
        all_flags_off = True
        for flag in _flags:
            if flag:
                all_flags_off = False
                break

        flags = list(_flags)

        if all_flags_off:
            flags[0] = True

        for filter_constructor, flag in zip(FILTERS, flags):
            if flag:
                return filter_constructor(expression)

        assert False, 'Unknown filter type'

    def run(self):
        self._run(self._folder_path, 0)

    def _run(self, folder_path, indent_level=0):
        with os.scandir(folder_path) as it:
            for entry in it:
                if entry.is_dir():
                    self._run(
                            os.path.join(folder_path, entry.name),
                            indent_level+1)
                elif self._is_request_file(entry):
                    self._print_request(entry.path)

    @staticmethod
    def _is_request_file(entry: str) -> bool:
        is_not_env = '__environment__' not in entry.name
        is_yaml = entry.name.endswith(('.yaml', '.yml'))

        return entry.is_file() and is_not_env and is_yaml

    def _print_request(self, request_file_name):
        request_name = request_file_name[self._base_path_length:-5]

        if not self._filter.filter(request_name):
            return

        with open(request_file_name) as request_file:
            import yaml

            request = yaml.safe_load(request_file)

        method = request['request']['method']

        print(f'{method.upper().ljust(7)} {request_name}')


class AbstractFilter(object):

    def __init__(self, expression):
        self._expression = self._get_expression(expression)
        log.info(f'Filtering expressions with {self.__class__}, expression {self._expression}')

    def _get_expression(self, expression):
        return expression

    def filter(self, request_name):
        return True


class GlobFilter(AbstractFilter):

    def filter(self, request_name):
        return fnmatch.fnmatch(request_name, self._expression)


class AsteriskGlobFilter(GlobFilter):

    def _get_expression(self, expression):
        return super()._get_expression(expression) + '*'


class RegexFilter(GlobFilter):

    def filter(self, request_name):
        return re.match(self._expression, request_name)
