# Standard library
import logging
import re
from typing import Any, Dict

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
    files_data: Dict[str, Any],
    project_name: str
) -> SimplePayloadType:
    success = False
    files_data = {
        re.sub(r'_([a-z])', lambda x: x.group(1).upper(), k): v
        for k, v in files_data.items()
    }
    file_name = files_data.get('fileName')
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    remove_file = await resources_domain.remove_file(
        str(file_name),
        project_name
    )
    if remove_file:
        await resources_domain.send_mail(
            project_name,
            user_email,
            [files_data],
            'removed',
            'file'
        )
        success = True
    else:
        LOGGER.error(
            'Couldn\'t remove file',
            extra={
                'extra': {
                    'file_name': file_name,
                    'project_name': project_name,
                }
            })
    if success:
        resource_utils.clean_cache(project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Removed Files from {project_name} project successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to remove files from {project_name} project'
        )

    return SimplePayloadType(success=success)
