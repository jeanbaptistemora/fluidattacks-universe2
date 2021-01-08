# Standard library
import logging
from typing import (
    Any,
    Dict,
    List
)

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import resources as resources_domain
from backend.typing import SimplePayload as SimplePayloadType
from backend.utils import resources as resource_utils

LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    envs: List[Dict[str, str]],
    project_name: str
) -> SimplePayloadType:
    new_envs = util.camel_case_list_dict(envs)
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    success = await resources_domain.create_environments(
        new_envs, project_name, user_email
    )

    if success:
        resource_utils.clean_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Added envs to {project_name} project successfully'
        )
        await resources_domain.send_mail(
            project_name,
            user_email,
            new_envs,
            'added',
            'environment'
        )
    else:
        LOGGER.error('Couldn\'t add environments', extra={'extra': locals()})
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add envs to {project_name} project'
        )

    return SimplePayloadType(success=success)
