from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SignPostUrlsPayload,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from newutils import (
    logs as logs_utils,
    resources as resources_utils,
)
from typing import (
    Any,
)

LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@require_login
async def mutate(
    _: Any, info: GraphQLResolveInfo, group_name: str, **parameters: Any
) -> SignPostUrlsPayload:
    success = False
    files_data = parameters["files_data"]

    signed_url = await resources_utils.upload_file(
        files_data[0]["file_name"], f"non_clients/{group_name}"
    )

    if signed_url:
        msg = (
            f'Security: Uploaded file {parameters["files_data"]} '
            f"for requester {group_name} successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
        success = True
    else:
        LOGGER.error(
            "Couldn't generate signed URL", extra={"extra": parameters}
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: A Requester attempted to add resource files "
            f"from {group_name} group",
        )

    return SignPostUrlsPayload(
        success=success,
        url={
            **signed_url,
            "fields": {
                **signed_url["fields"],
                "awsaccesskeyid": signed_url["fields"]["AWSAccessKeyId"],
            },
        },
    )
