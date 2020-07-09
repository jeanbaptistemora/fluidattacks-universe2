# Standard library
import asyncio
import contextlib
from datetime import datetime
from decimal import Decimal
import functools
import json
import os
from typing import (
    Any,
    AsyncIterator,
    Callable,
    Dict,
    Iterator,
    List,
    Tuple,
    Type,
    Union,
)
from urllib.parse import (
    quote_plus,
    urlparse,
)

# Third party libraries
from backend.domain import (
    organization as org_domain,
    project as group_domain,
    forces as forces_domain,
)
from frozendict import frozendict


async def get_all_time_forces_executions(
    group: str,
) -> List[Dict[str, Union[str, int]]]:
    executions: List[Dict[str, Union[str, int]]]
    executions = await forces_domain.get_executions(
        from_date=datetime.utcfromtimestamp(1),
        group_name=group,
        to_date=datetime.utcnow(),
    )

    return executions


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
    where: str = vulnerability['where'].strip()

    if kind == 'lines':
        root: str = get_repo_from_where(where)
    elif kind == 'ports':
        root = where
    elif kind == 'inputs':
        try:
            url = urlparse(where)
        except ValueError:
            root = where
        else:
            root = url.hostname or where
    else:
        root = where

    return root


def iterate_groups() -> Iterator[str]:
    for group in sorted(group_domain.get_alive_projects(), reverse=True):
        log_info(f'Working on group: {group}')
        yield group


async def iterate_organizations_and_groups() -> AsyncIterator[
    Tuple[str, str, Tuple[str, ...]],
]:
    """Yield (org_id, org_name, org_groups) non-concurrently generated."""
    async for org_id, org_name, org_groups in (
        org_domain.iterate_organizations_and_groups()
    ):
        log_info(f'Working on organization: {org_id} ({org_name})')

        yield org_id, org_name, org_groups


def json_dump(
    *,
    document: object,
    entity: str,
    subject: str,
) -> None:
    for result_path in map(get_result_path, [
        # Backwards compatibility
        f'{entity}-{subject}.json',
        # New format
        f'{quote_plus(entity)}:{quote_plus(subject)}.json',
    ]):
        with open(result_path, 'w') as file:
            json.dump(document, file, default=json_encoder, indent=2)


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


# Using Any because this is a generic-input decorator
def retry_on_exceptions(
    *,
    default_value: Any,
    exceptions: Tuple[Type[Exception], ...],
    retry_times: int,
) -> Callable[..., Any]:

    def decorator(function: Callable[..., Any]) -> Callable[..., Any]:

        if asyncio.iscoroutinefunction(function):
            @functools.wraps(function)
            async def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(retry_times):
                    with contextlib.suppress(*exceptions):
                        return await function(*args, **kwargs)

                return default_value
        else:
            @functools.wraps(function)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                for _ in range(retry_times):
                    with contextlib.suppress(*exceptions):
                        return function(*args, **kwargs)

                return default_value

        return wrapper

    return decorator
