from asgiref.sync import sync_to_async
from backend.decorators import (
    enforce_user_level_auth_async,
    require_login,
)
from backend.domain import internal_project as internal_project_domain
from backend.typing import InternalProject as InternalProjectType

from ariadne import convert_kwargs_to_snake_case


async def _resolve_fields() -> InternalProjectType:
    """Async resolve fields."""
    name = await sync_to_async(internal_project_domain.get_project_name)()
    result: InternalProjectType = dict()
    result['project_name'] = name
    return result


@convert_kwargs_to_snake_case
@require_login
@enforce_user_level_auth_async
async def resolve_project_name(*_) -> InternalProjectType:
    """Resolve internalProjectNames query."""
    return await _resolve_fields()
