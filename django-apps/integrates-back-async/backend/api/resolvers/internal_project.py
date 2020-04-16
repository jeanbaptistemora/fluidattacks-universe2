# pylint: disable=import-error

import asyncio
from typing import Dict

from asgiref.sync import sync_to_async
from backend.decorators import (
    enforce_user_level_auth_async,
    require_login,
)
from backend.domain import internal_project as internal_project_domain
from backend.typing import InternalProject as InternalProjectType
from backend import util

from ariadne import convert_kwargs_to_snake_case


@sync_to_async
def _get_project_name() -> Dict[str, str]:
    """Get remember preference."""
    name = internal_project_domain.get_project_name()
    return dict(project_name=name)


async def _resolve_fields() -> InternalProjectType:
    """Async resolve fields."""
    result: InternalProjectType = dict()
    future = asyncio.ensure_future(
        _get_project_name()
    )
    tasks_result = await asyncio.gather(future)
    for dict_result in tasks_result:
        result.update(dict_result)
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
def resolve_project_name(*_) -> InternalProjectType:
    """Resolve internalProjectNames query."""
    return util.run_async(_resolve_fields)
