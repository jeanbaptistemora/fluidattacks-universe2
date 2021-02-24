# Standard library
import logging
from typing import Any

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
from backend.utils import (
    virus_scan
)

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
    **parameters: Any
) -> SimplePayloadType:
    success = False
    files_data = parameters['files_data']
    new_files_data = util.camel_case_list_dict(files_data)
    uploaded_file = parameters['file']
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    project_name = parameters['project_name']

    virus_scan.scan_file(uploaded_file, user_email, project_name)

    add_file = await resources_domain.create_file(
        new_files_data,
        uploaded_file,
        project_name,
        user_email
    )
    if add_file:
        await resources_domain.send_mail(
            info.context.loaders,
            project_name,
            user_email,
            new_files_data,
            'added',
            'file'
        )

        success = True
    else:
        LOGGER.error('Couldn\'t upload file', extra={'extra': parameters})
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Added resource files to {project_name} '
            f'project successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add resource files '
            f'from {project_name} project'
        )

    return SimplePayloadType(success=success)
