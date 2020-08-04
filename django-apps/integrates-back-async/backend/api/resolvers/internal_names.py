from typing import Any

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import (
    enforce_user_level_auth_async,
    require_login,
)
from backend.domain import available_name as available_name_domain
from backend.typing import InternalName as InternalNameType


async def _resolve_fields(entity: str) -> InternalNameType:
    """Async resolve fields."""
    name = await available_name_domain.get_name(entity)
    result: InternalNameType = dict()
    result['name'] = name
    return result


@convert_kwargs_to_snake_case  # type: ignore
@require_login
@enforce_user_level_auth_async
async def resolve_project_name(
        _: Any,
        __: GraphQLResolveInfo,
        entity: str,
        *___: Any) -> InternalNameType:
    """Resolve InternalNameNames query."""
    return await _resolve_fields(entity)
