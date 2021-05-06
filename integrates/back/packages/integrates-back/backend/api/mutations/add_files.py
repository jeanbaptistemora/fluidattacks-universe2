# Standard library
import logging
from typing import Any

# Third party libraries
from aioextensions import schedule
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.typing import SimplePayload as SimplePayloadType
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from mailer import resources as resources_mail
from newutils import virus_scan
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
        schedule(
            resources_mail.send_mail_update_resource(
                info.context.loaders,
                project_name,
                user_email,
                new_files_data,
                'added',
                'file'
            )
        )
        success = True
    else:
        LOGGER.error('Couldn\'t upload file', extra={'extra': parameters})
    if success:
        info.context.loaders.group.clear(project_name)
        info.context.loaders.group_all.clear(project_name)
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
