import logging
import re
import sys
from typing import Any, Dict, cast, Union

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from backend.decorators import (
    concurrent_decorators,
    require_login,
    require_integrates,
    enforce_group_level_auth_async
)
from backend.domain import resources
from backend.typing import (
    Resource as ResourceType,
    DownloadFilePayload as DownloadFilePayloadType,
    SimplePayload as SimplePayloadType,
)
from backend import util

from back.settings import LOGGING

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def _clean_resources_cache(project_name: str) -> None:
    util.queue_cache_invalidation(
        # resource entity related
        f'environments*{project_name}',
        f'files*{project_name}',
        # project entity related
        f'has*{project_name}',
        f'deletion*{project_name}',
        f'tags*{project_name}',
        f'subscription*{project_name}',
    )


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_resources_mutation(
    obj: Any,
    info: GraphQLResolveInfo,
    **parameters: Any
) -> Union[SimplePayloadType, DownloadFilePayloadType]:
    """Wrap resources mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_update_environment(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        env: Dict[str, str],
        state: str) -> SimplePayloadType:
    """Resolve update_environment mutation."""
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    env = {
        re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
        for k, v in env.items()
    }
    success = await resources.update_resource(
        cast(ResourceType, env),
        project_name,
        'environment',
        user_email
    )

    if success:
        _clean_resources_cache(project_name)
        util.cloudwatch_log(
            info.context,
            (f'Security: Updated environment state in {project_name} '
             'project successfully')  # pragma: no cover
        )

        action = 'activated' if state == 'ACTIVE' else 'deactivated'
        await resources.send_mail(
            project_name,
            user_email,
            [cast(Dict[str, object], env)],
            action,
            'environment'
        )
    else:
        LOGGER.error(
            'Couldn\'t update environment state', extra={'extra': locals()})
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to update environment state in '
             f'{project_name} project')  # pragma: no cover
        )
    return SimplePayloadType(success=success)
