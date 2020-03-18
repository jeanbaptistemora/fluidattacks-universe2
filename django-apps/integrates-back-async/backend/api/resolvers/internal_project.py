# pylint: disable=import-error

import asyncio

from backend.decorators import require_login, enforce_authz_async

from backend.domain import internal_project as internal_project_domain

from ariadne import convert_kwargs_to_snake_case


async def _get_project_name():
    """Get remember preference."""
    name = internal_project_domain.get_project_name()
    return dict(project_name=name)


async def _resolve_fields():
    """Async resolve fields."""
    result = dict()
    future = asyncio.ensure_future(
        _get_project_name()
    )
    tasks_result = await asyncio.gather(future)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_authz_async
def resolve_project_name(*_):
    """Resolve internalProjectNames query."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        _resolve_fields()
    )
    loop.close()
    return result
