# pylint: disable=import-error

import asyncio
import sys

from asgiref.sync import sync_to_async
from backend.decorators import (
    require_login, require_project_access,
    enforce_authz_async
)
from backend.domain import project as project_domain
from backend.exceptions import InvalidProject

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake


@sync_to_async
def _get_repositories(project_name: str):
    """Get repositories."""
    project_info = project_domain.get_attributes(
        project_name, ['repositories']
    )
    return dict(repositories=project_info.get('repositories', []))


@sync_to_async
def _get_environments(project_name: str):
    """Get environments."""
    project_info = project_domain.get_attributes(
        project_name, ['environments']
    )
    return dict(environments=project_info.get('environments', []))


@sync_to_async
def _get_files(project_name: str):
    """Get files."""
    project_info = project_domain.get_attributes(
        project_name, ['files']
    )
    return dict(files=project_info.get('files', []))


async def _resolve_fields(info, project_name):
    """Async resolve fields."""
    result = dict(
        repositories=list(),
        environments=list(),
        files=list()
    )
    tasks = list()
    project_name = project_name.lower()

    project_exist = project_domain.get_attributes(
        project_name, ['project_name']
    )
    if not project_exist:
        raise InvalidProject
    for requested_field in info.field_nodes[0].selection_set.selections:
        snk_fld = convert_camel_case_to_snake(requested_field.name.value)
        if snk_fld.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{snk_fld}'
        )
        future = asyncio.ensure_future(resolver_func(project_name))
        tasks.append(future)
    tasks_result = await asyncio.gather(*tasks)
    for dict_result in tasks_result:
        result.update(dict_result)

    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
@require_project_access
def resolve_resources(_, info, project_name):
    """Resolve resources query."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        _resolve_fields(info, project_name)
    )
    loop.close()
    return result
