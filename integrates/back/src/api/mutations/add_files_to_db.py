from ariadne import (
    convert_kwargs_to_snake_case,
)
from batch.dal import (
    put_action,
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
from newutils.utils import (
    get_key_or_fallback,
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
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayloadType:
    success = False
    files_data = parameters["files_data"]
    new_files_data = utils.camel_case_list_dict(files_data)
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    group_name: str = get_key_or_fallback(parameters)

    await put_action(
        action_name="handle_virus_scan",
        entity=group_name,
        subject=user_email,
        additional_info=files_data[0]["file_name"],
        queue="dedicated_soon",
    )

    success = await add_file_to_db(new_files_data, group_name, user_email)

    if success:
        msg = (
            f'Security: Added file {parameters["files_data"]}'
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
