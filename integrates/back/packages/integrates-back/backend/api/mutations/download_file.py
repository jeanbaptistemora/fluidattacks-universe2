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
from backend.typing import DownloadFilePayload as DownloadFilePayloadType
from backend.utils import analytics

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
) -> DownloadFilePayloadType:
    success = False
    file_info = parameters['files_data']
    project_name = parameters['project_name'].lower()
    user_info = await util.get_jwt_content(info.context)
    user_email = user_info['user_email']
    signed_url = await resources_domain.download_file(
        file_info, project_name
    )
    if signed_url:
        msg = (
            f'Security: Downloaded file {parameters["files_data"]} '
            f'in project {project_name} successfully'
        )
        util.cloudwatch_log(info.context, msg)
        await analytics.mixpanel_track(
            user_email,
            'DownloadProjectFile',
            Project=project_name.upper(),
            FileName=parameters['files_data'],
        )
        success = True
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to download file '
            f'{parameters["files_data"]} in project {project_name}'
        )
        LOGGER.error(
            'Couldn\'t generate signed URL',
            extra={'extra': parameters}
        )

    return DownloadFilePayloadType(success=success, url=str(signed_url))
