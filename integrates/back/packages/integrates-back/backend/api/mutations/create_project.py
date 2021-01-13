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
from backend.domain import project as project_domain
from backend.typing import SimplePayload as SimplePayloadType
from backend.utils.user import create_forces_user


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
    user_data = await util.get_jwt_content(info.context)
    user_email = user_data['user_email']
    user_role = await authz.get_user_level_role(user_email)

    success = await project_domain.create_project(
        user_email,
        user_role,
        project_name.lower(),
        organization,
        description,
        has_drills,
        has_forces,
        subscription,
        language,
    )

    if success and has_forces:
        await create_forces_user(info, project_name)
    if success:
        util.queue_cache_invalidation(user_email)
        util.cloudwatch_log(
            info.context,
            f'Security: Created project {project_name.lower()} successfully',
        )

    return SimplePayloadType(success=success)
