from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
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
    logs as logs_utils,
    token as token_utils,
    utils,
    virus_scan,
)
from newutils.utils import (
    resolve_kwargs,
)
from resources import (
    domain as resources_domain,
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
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayloadType:
    files_data = parameters["files_data"]
    new_files_data = utils.camel_case_list_dict(files_data)
    uploaded_file = parameters["file"]
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    group_name: str = resolve_kwargs(parameters)

    virus_scan.scan_file(uploaded_file, user_email, group_name)

    success = await resources_domain.create_file(
        new_files_data, uploaded_file, group_name, user_email
    )
    if success:
        info.context.loaders.group.clear(group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added resource files to {group_name} "
            f"group successfully",
        )
    else:
        LOGGER.error("Couldn't upload file", extra={"extra": parameters})
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add resource files "
            f"from {group_name} group",
        )

    return SimplePayloadType(success=success)
