import os
import yaml


def request_file(home_folder, request_name: str) -> str:
    # FIXME Will not work on Windows due to /'s
    return os.path.join(home_folder, request_name + '.yaml')


def _environment_file(home_folder, folders: list) -> str:
    return os.path.join(home_folder, *folders, '__environment__.yaml')


def _get_raw_environment_data(home_folder, folders):
    environmentFile = _environment_file(home_folder, folders)

    if not os.path.exists(environmentFile):
        return {}

    with open(environmentFile) as f:
        return yaml.safe_load(f)


def _get_environment(raw, name):
    for environment in raw.get('environments', []):
        if environment.get('name', '') == name:
            return environment

    return {}


def _format_all_strs_on_dict(home_folder: str, environment: dict, d: dict) -> dict:
    for key, value in dict(d).items():
        formatted = _format_all_strs(home_folder, environment, value)

        if formatted != value:
            d[key] = formatted

    return d


def _format_all_strs(home_folder: str, environment: dict, obj: object) -> dict:
    if isinstance(obj, dict):
        return _format_all_strs_on_dict(home_folder, environment, obj)

    if isinstance(obj, str):
        # FIXME Cant be with @ at beginning, use regex: \{file:[a-z0-9\-_/]\}
        # FIXME This must be done BEFORE any other interpolation, split this
        # phase
        if obj.startswith('@'):
            file_path = os.path.join(home_folder, obj[1:] + '.data')
            with open(file_path) as f:
                return '\n'.join(f.readlines()).strip()
        else:
            return obj.format(**environment)

    return obj


def _load_environment(home_folder, environment_name, request_name):
    concrete = dict()

    folders = request_name.split('/')
    for i in range(len(folders)):
        abstract = _get_raw_environment_data(home_folder, folders[:i])

        if environment_name == '':
            environment_name = abstract.get('selected', '')

        concrete.update(_get_environment(abstract, environment_name))

    # FIXME This should only load external files, not inject environment into
    # itself
    return _format_all_strs_on_dict(home_folder, concrete, dict(concrete))


def _get_raw_request_data(home_folder, request_name):
    with open(request_file(home_folder, request_name)) as f:
        return yaml.safe_load(f)


def _build_request(home_folder: str, data: dict, environment: dict) -> dict:
    request = dict(data['request'])

    request = _format_all_strs_on_dict(home_folder, environment, request)

    return request


def create_request(home_folder: str, environment: str, request_name: str) -> dict:
    environment = _load_environment(home_folder, environment, request_name)

    raw_data = _get_raw_request_data(home_folder, request_name)

    return _build_request(home_folder, raw_data, environment), raw_data
