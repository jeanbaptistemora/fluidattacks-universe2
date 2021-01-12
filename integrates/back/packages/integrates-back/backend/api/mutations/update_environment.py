# Standard library
import logging
import re
from typing import (
    Any,
    cast,
    Dict
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
from backend.typing import (
    Resource as ResourceType,
    SimplePayload as SimplePayloadType
)
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
    project_name: str,
    env: Dict[str, str],
    state: str
) -> SimplePayloadType:
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    env = {
        re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
        for k, v in env.items()
    }
    success = await resources_domain.update_resource(
        cast(ResourceType, env),
        project_name,
        'environment',
        user_email
    )

    if success:
        resource_utils.clean_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Updated environment state in '
            f'{project_name} project successfully'
        )

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        await resources_domain.send_mail(
            project_name,
            user_email,
            [cast(Dict[str, object], env)],
            action,
            'environment'
        )
    else:
        LOGGER.error(
            'Couldn\'t update environment state',
            extra={'extra': locals()}
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to update environment state '
            f'in {project_name} project'
        )

    return SimplePayloadType(success=success)
