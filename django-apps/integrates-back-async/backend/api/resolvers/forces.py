from datetime import datetime
import sys
from typing import List, Any, Union

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake
from asgiref.sync import sync_to_async

from backend.decorators import (
    enforce_group_level_auth_async, get_entity_cache_async, require_login,
    require_integrates
)
from backend.domain import (
    forces as forces_domain,
)
from backend.typing import (
    ForcesExecution as ForcesExecutionType,
    ForcesExecutions as ForcesExecutionsType,
)
from backend import util
from graphql.type.definition import GraphQLResolveInfo


@sync_to_async  # type: ignore
def _get_project_name(
        _: GraphQLResolveInfo,
        project_name: str,
        **__: datetime) -> str:
    """Get project_name."""
    return project_name


@sync_to_async  # type: ignore
def _get_from_date(
        _: GraphQLResolveInfo,
        from_date: datetime,
        **__: Union[datetime, str]) -> datetime:
    """Get from_date."""
    return from_date


@sync_to_async  # type: ignore
def _get_to_date(
        _: GraphQLResolveInfo,
        to_date: datetime,
        **__: Union[datetime, str]) -> datetime:
    """Get to_date."""
    return to_date


@get_entity_cache_async
async def _get_executions(
        _: GraphQLResolveInfo,
        project_name: str,
        from_date: datetime,
        to_date: datetime) -> List[ForcesExecutionType]:
    """Get executions."""
    return await forces_domain.get_executions(
        from_date=from_date,
        group_name=project_name,
        to_date=to_date
    )


async def _resolve_fields(
        info: GraphQLResolveInfo,
        project_name: str,
        from_date: datetime,
        to_date: datetime) -> ForcesExecutionsType:
    """Async resolve fields."""
    result: ForcesExecutionsType = dict()
    for requested_field in info.field_nodes[0].selection_set.selections:
        snake_field = convert_camel_case_to_snake(requested_field.name.value)
        if snake_field.startswith('_'):
            continue
        resolver_func = getattr(
            sys.modules[__name__],
            f'_get_{snake_field}'
        )
        result[snake_field] = resolver_func(
            info,
            project_name=project_name,
            from_date=from_date,
            to_date=to_date
        )
    return result


@convert_kwargs_to_snake_case  # type: ignore
@require_login
@enforce_group_level_auth_async
@require_integrates
async def resolve_forces_executions(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        from_date: Union[datetime, None] = None,
        to_date: Union[datetime, None] = None) -> ForcesExecutionsType:
    """Resolve forces_executions query."""
    project_name = project_name.lower()
    from_date = from_date or util.get_current_time_minus_delta(weeks=1)
    to_date = to_date or datetime.utcnow()
    return await _resolve_fields(info, project_name, from_date, to_date)
