import logging
import logging.config
from typing import Any

from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import DownloadFilePayload as DownloadFilePayloadType
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from newutils import (
    analytics,
    logs as logs_utils,
    resources as resources_utils,
    token as token_utils,
)


LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> DownloadFilePayloadType:
    success = False
    file_info = parameters["files_data"]
    project_name = parameters["project_name"].lower()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    signed_url = await resources_utils.download_file(file_info, project_name)
    if signed_url:
        msg = (
            f'Security: Downloaded file {parameters["files_data"]} '
            f"in project {project_name} successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
        await analytics.mixpanel_track(
            user_email,
            "DownloadProjectFile",
            Project=project_name.upper(),
            FileName=parameters["files_data"],
        )
        success = True
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to download file "
            f'{parameters["files_data"]} in project {project_name}',
        )
        LOGGER.error(
            "Couldn't generate signed URL", extra={"extra": parameters}
        )

    return DownloadFilePayloadType(success=success, url=str(signed_url))
