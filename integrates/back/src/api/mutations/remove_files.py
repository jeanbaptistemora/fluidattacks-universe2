from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorUpdatingGroup,
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
)
import re
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
    files_data: dict[str, Any],
    group_name: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    files_data = {
        re.sub(r"_([a-z])", lambda x: x.group(1).upper(), k): v
        for k, v in files_data.items()
    }
    file_name = str(files_data.get("fileName"))
    group_name = group_name.lower()
    try:
        await groups_domain.remove_file(
            loaders=loaders,
            group_name=group_name,
            file_name=file_name,
        )
    except ErrorUpdatingGroup:
        LOGGER.error(
            "Couldn't remove file",
            extra={
                "extra": {
                    "file_name": file_name,
                    "group_name": group_name,
                }
            },
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove files from {group_name} group",
        )
        raise

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Removed files from {group_name} group successfully",
    )
    return SimplePayload(success=True)
