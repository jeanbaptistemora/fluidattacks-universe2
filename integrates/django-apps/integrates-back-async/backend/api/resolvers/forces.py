import sys
from typing import (
    Any,
    cast,
    Union
)

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

from backend.decorators import (
    enforce_group_level_auth_async,
    require_forces,
)
from backend.domain import (
    forces as forces_domain,
    user as user_domain
)
from backend.typing import (
    SimplePayload as SimplePayloadType,
    UpdateAccessTokenPayload as UpdateAccessTokenPayloadType,
)
from backend.utils import (
    datetime as datetime_utils,
)
from backend.exceptions import InvalidExpirationTime
from backend import util


@enforce_group_level_auth_async
async def _do_add_forces_execution(_: Any,
                                   info: GraphQLResolveInfo,
                                   project_name: str,
                                   log: Union[UploadFile,
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
