# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import authz, util
from backend.decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login
)
from backend.domain import project as group_domain
from backend.typing import SimplePayload as SimplePayloadType
from forces import domain as forces_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(  # pylint: disable=too-many-arguments
    _: Any,
    info: GraphQLResolveInfo,
    description: str,
    organization: str,
    project_name: str,
    subscription: str = 'continuous',
    has_drills: bool = False,
    has_forces: bool = False,
    language: str = 'en'
) -> SimplePayloadType:
    group_name = project_name
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    user_role = await authz.get_user_level_role(user_email)

    success = await group_domain.create_group(
        user_email,
        user_role,
        group_name.lower(),
        organization,
        description,
        has_drills,
        has_forces,
        subscription,
        language,
    )

    if success and has_forces:
        info.context.loaders.group_all.clear(group_name)
        await forces_domain.create_forces_user(info, group_name)
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Created group {group_name.lower()} successfully',
        )

    return SimplePayloadType(success=success)
