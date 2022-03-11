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
)
from resources.domain import (
    add_file_to_db,
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
    _: Any, info: GraphQLResolveInfo, group_name: str, **parameters: Any
) -> SimplePayloadType:
    success = False
    files_data = parameters["files_data"]
    new_files_data = utils.camel_case_list_dict(files_data)
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    success = await add_file_to_db(new_files_data, group_name, user_email)

    if success:
        msg = (
            f'Security: Added file {parameters["files_data"]} '
            f"to db in group {group_name} successfully"
        )
        logs_utils.cloudwatch_log(info.context, msg)
    else:
        LOGGER.error(
            "Couldn't add the file to the db", extra={"extra": parameters}
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add resource files "
            f"from {group_name} group",
        )

    return SimplePayloadType(success=success)
