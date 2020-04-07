# pylint: disable=import-error

from datetime import datetime
from functools import reduce
import asyncio
import sys

from asgiref.sync import sync_to_async
from backend.decorators import (
    enforce_group_level_auth_async, require_login,
    require_project_access
)
from backend.dal import forces as forces_dal
from backend import util

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


def match_fields(my_dict):
    """Replace fields from response according to schema."""
    replace_tuple = (
        ('vulnerability_count_mocked_exploits',
         'num_of_vulnerabilities_in_mocked_exploits'),
        ('vulnerability_count_exploits',
         'num_of_vulnerabilities_in_exploits'),
        ('vulnerability_count_accepted_exploits',
         'num_of_vulnerabilities_in_accepted_exploits')
    )
    new = {}
    for key, val in my_dict.items():
        if isinstance(val, dict):
            val = match_fields(val)
        new[reduce(lambda a, kv: a.replace(*kv), replace_tuple, key)] = val
    return new


@sync_to_async
def _get_project_name(project_name, **_):
    """Get project_name."""
    return dict(project_name=project_name)


@sync_to_async
def _get_from_date(from_date, **_):
    """Get from_date."""
    return dict(from_date=from_date)


@sync_to_async
def _get_to_date(to_date, **_):
    """Get to_date."""
    return dict(to_date=to_date)


@sync_to_async
def _get_executions(project_name, from_date, to_date):
    """Get executions."""
    executions_iterator = forces_dal.yield_executions(
        project_name=project_name,
        from_date=from_date,
        to_date=to_date
    )
    res = [
        match_fields(execution) for execution in executions_iterator
    ]
    return dict(executions=res)


async def _resolve_fields(info, project_name, from_date, to_date):
    """Async resolve fields."""
    result = dict()
    tasks = list()
    for requested_field in info.field_nodes[0].selection_set.selections:
        snake_field = convert_camel_case_to_snake(requested_field.name.value)
        if snake_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{snake_field}'
        )
        future = asyncio.ensure_future(
            resolver_func(project_name=project_name,
                          from_date=from_date,
                          to_date=to_date)
        )
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_group_level_auth_async
@require_project_access
def resolve_forces_executions(
    _, info, project_name, from_date=None, to_date=None
):
    """Resolve forces_executions query."""
    project_name = project_name.lower()
    from_date = from_date or util.get_current_time_minus_delta(weeks=1)
    to_date = to_date or datetime.utcnow()
    return util.run_async(
        _resolve_fields, info, project_name, from_date, to_date
    )
