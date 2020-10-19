from datetime import datetime
import sys
from typing import (
    Any,
    cast,
    List,
    Union
)

from ariadne import convert_kwargs_to_snake_case, convert_camel_case_to_snake
from django.core.files.uploadedfile import InMemoryUploadedFile
from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_forces,
    require_integrates,
    require_login,
)
from backend.domain import (
    forces as forces_domain,
    user as user_domain
)
from backend.typing import (
    ForcesExecution as ForcesExecutionType,
    ForcesExecutions as ForcesExecutionsType,
    SimplePayload as SimplePayloadType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from backend.utils import (
    datetime as datetime_utils,
)
from backend.exceptions import InvalidExpirationTime
from backend import util


async def _get_project_name(
        _: GraphQLResolveInfo,
        project_name: str,
        **__: datetime) -> str:
    """Get project_name."""
    return project_name


async def _get_from_date(
        _: GraphQLResolveInfo,
        from_date: datetime,
        **__: Union[datetime, str]) -> datetime:
    """Get from_date."""
    return from_date


async def _get_to_date(
        _: GraphQLResolveInfo,
        to_date: datetime,
        **__: Union[datetime, str]) -> datetime:
    """Get to_date."""
    return to_date


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


@enforce_group_level_auth_async
async def _do_add_forces_execution(_: Any,
                                   info: GraphQLResolveInfo,
                                   project_name: str,
                                   log: Union[InMemoryUploadedFile,
                                              None] = None,
                                   **parameters: Any) -> SimplePayloadType:
    success = await forces_domain.add_forces_execution(
        project_name=project_name, log=log, **parameters)
    if success:
        util.cloudwatch_log(
            info.context,
            ('Security: Created forces execution in '
             f'{project_name} project successfully')  # pragma: no cover
        )
    return SimplePayloadType(success=success)


@convert_kwargs_to_snake_case  # type: ignore
@require_forces
async def resolve_forces_execution_mutation(
    obj: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> Union[
    SimplePayloadType
]:
    """Wrap forces executions mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return cast(
        Union[
            SimplePayloadType
        ],
        await resolver_func(obj, info, **parameters)
    )


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve_forces_executions(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        from_date: Union[datetime, None] = None,
        to_date: Union[datetime, None] = None) -> ForcesExecutionsType:
    """Resolve forces_executions query."""
    project_name = project_name.lower()
    from_date = from_date or datetime_utils.get_now_minus_delta(weeks=1)
    to_date = to_date or datetime_utils.get_now()
    return await _resolve_fields(info, project_name, from_date, to_date)


@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def update_forces_access_token(
        _: Any, info: GraphQLResolveInfo,
        project_name: str) -> UpdateAccessTokenPayloadType:
    """Resolve update_access_token mutation."""
    user_info = await util.get_jwt_content(info.context)

    user_email = user_domain.format_forces_user_email(project_name)
    if not user_domain.ensure_user_exists(user_email):
        util.cloudwatch_log(
            info.context,
            (
                f'{user_info["user_email"]} '  # pragma: no cover
                'try to update token for a user forces that does not exist'
                f' {user_email}'),
        )
        return UpdateAccessTokenPayloadType(success=False, session_jwt='')

    expiration_time = int(
        datetime_utils.get_now_plus_delta(days=180).timestamp()
    )
    try:
        result = await user_domain.update_access_token(
            user_email,
            expiration_time,
        )
        if result.success:
            util.cloudwatch_log(
                info.context,
                (
                    f'{user_info["user_email"]} '  # pragma: no cover
                    f'update access token for {user_email}'),
            )
        else:
            util.cloudwatch_log(
                info.context,
                (
                    f'{user_info["user_email"]} '  # pragma: no cover
                    f'attempted to update access token for {user_email}'),
            )
        return result
    except InvalidExpirationTime as exc:
        util.cloudwatch_log(
            info.context,
            (
                f'{user_info["user_email"]} '  # pragma: no cover
                'attempted to use expiration time '
                'greater than six months or minor '
                'than current time'),
        )
        raise exc
