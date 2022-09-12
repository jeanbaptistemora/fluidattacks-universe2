# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    DownloadFilePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorDownloadingFile,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from newutils import (
    analytics,
    logs as logs_utils,
    resources as resources_utils,
    token as token_utils,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str, **parameters: Any
) -> DownloadFilePayload:
    file_info = parameters["files_data"]
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    signed_url = await resources_utils.download_file(file_info, group_name)
    if signed_url:
        msg = (
            f'Security: Downloaded file {parameters["files_data"]} '
            f"in group {group_name} successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
        await analytics.mixpanel_track(
            user_email,
            "DownloadGroupFile",
            Group=group_name.upper(),
            FileName=parameters["files_data"],
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to download file "
            f'{parameters["files_data"]} in group {group_name}',
        )
        LOGGER.error(
            "Couldn't generate signed URL", extra={"extra": parameters}
        )
        raise ErrorDownloadingFile()

    return DownloadFilePayload(success=True, url=str(signed_url))
