from .payloads.types import (
    SignPostUrlsPayload,
)
from .schema import (
    MUTATION,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorUploadingFileS3,
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
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@MUTATION.field("signPostUrl")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str, **parameters: Any
) -> SignPostUrlsPayload:
    files_data = parameters["files_data"]
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    signed_url = await resources_utils.upload_file(
        file_info=files_data[0]["file_name"], group_name=group_name
    )

    if signed_url:
        msg = (
            f'Security: Uploaded file {parameters["files_data"]} '
            f"in group {group_name} successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
        await analytics.mixpanel_track(
            user_email,
            "UploadGroupFile",
            Group=group_name.upper(),
            FileName=parameters["files_data"],
        )
    else:
        LOGGER.error(
            "Couldn't generate signed URL", extra={"extra": parameters}
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add resource files "
            f"from {group_name} group",
        )
        raise ErrorUploadingFileS3()

    return SignPostUrlsPayload(
        success=True,
        url={
            **signed_url,
            "fields": {
                **signed_url["fields"],
                "credential": signed_url["fields"]["x-amz-credential"],
                "signature": signed_url["fields"]["x-amz-signature"],
                "algorithm": signed_url["fields"]["x-amz-algorithm"],
                "date": signed_url["fields"]["x-amz-date"],
                "securitytoken": signed_url["fields"]["x-amz-security-token"],
            },
        },
    )
