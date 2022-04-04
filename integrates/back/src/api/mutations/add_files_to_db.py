from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorFileNameAlreadyExists,
    InvalidChar,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
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
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    logs as logs_utils,
    token as token_utils,
    utils,
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
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = str(group_name).lower()
    files_data = kwargs["files_data"]
    new_files_data = utils.camel_case_list_dict(files_data)
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    try:
        for file_data in new_files_data:
            await groups_domain.add_file(
                loaders=loaders,
                description=file_data["description"],
                file_name=file_data["fileName"],
                group_name=group_name,
                user_email=user_email,
            )
    except (InvalidChar, ErrorFileNameAlreadyExists):
        LOGGER.error(
            "Couldn't add the file to the db", extra={"extra": kwargs}
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add resource files "
            f"from {group_name} group",
        )
        raise

    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Added file {kwargs["files_data"]} '
        f"to db in group {group_name} successfully",
    )

    return SimplePayload(success=True)
