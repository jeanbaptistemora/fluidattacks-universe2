# Standard library
from decimal import Decimal
import json
import os
from typing import (
    Any,
    Dict,
    Iterable,
)

# Third party libraries
from backend.domain import (
    project as group_domain,
)
from frozendict import frozendict


def get_result_path(name: str) -> str:
    return os.path.join(os.environ['RESULTS_DIR'], name)


def get_repo_from_where(where: str) -> str:
    if '/' in where:
        repo = where.split('/', 1)[0]
    elif '\\' in where:
        repo = where.split('\\', 1)[0]
    else:
        repo = where

    return repo


def get_vulnerability_source(vulnerability: Dict[str, str]) -> str:
    kind: str = vulnerability['vuln_type']
    where: str = vulnerability['where']

    if kind == 'lines':
        root: str = get_repo_from_where(where)
    elif kind == 'ports':
        root = where
    else:
        root = ''

    return root


def iterate_groups() -> Iterable[str]:
    for group in sorted(group_domain.get_alive_projects()):
        log_info(f'Working on {group}')
        yield group


def json_dump(name: str, data: object) -> None:
    result_path = get_result_path(name)

    with open(result_path, 'w') as file:
        json.dump(data, file, default=json_encoder, indent=2)


# Using Any because this is a generic-input function
def json_encoder(obj: Any) -> Any:
    obj_type: type = type(obj)

    if obj_type == set:
        casted_obj: Any = [
            json_encoder(value)
            for value in obj
        ]
    elif obj_type == frozendict:
        casted_obj = {
            key: json_encoder(value)
            for key, value in obj.items()
        }
    elif obj_type == Decimal:
        casted_obj = float(obj)
    else:
        casted_obj = obj

    return casted_obj


# Using Any because this is a generic-input function
def log_info(*args: Any, **kwargs: Any) -> None:
    print('[INFO]', *args, **kwargs)
