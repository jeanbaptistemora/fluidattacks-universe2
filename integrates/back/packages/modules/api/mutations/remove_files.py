
import logging
import logging.config
import re
from typing import (
    Any,
    Dict,
)

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload as SimplePayloadType
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from newutils import logs as logs_utils
from resources import domain as resources_domain


LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    files_data: Dict[str, Any],
    project_name: str
) -> SimplePayloadType:
    files_data = {
        re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
        for k, v in files_data.items()
    }
    file_name = files_data.get('fileName')
    success = await resources_domain.remove_file(
        str(file_name),
        project_name
    )
    if success:
        info.context.loaders.group.clear(project_name)
        info.context.loaders.group_all.clear(project_name)
        logs_utils.cloudwatch_log(
            info.context,
            f'Security: Removed Files from {project_name} project successfully'
        )
    else:
        LOGGER.error(
            'Couldn\'t remove file',
            extra={
                'extra': {
                    'file_name': file_name,
                    'project_name': project_name,
                }
            })
        logs_utils.cloudwatch_log(
            info.context,
            f'Security: Attempted to remove files from {project_name} project'
        )

    return SimplePayloadType(success=success)
