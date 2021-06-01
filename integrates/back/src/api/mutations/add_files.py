from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
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
    require_integrates,
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, **parameters: Any
) -> SimplePayloadType:
    files_data = parameters["files_data"]
    new_files_data = utils.camel_case_list_dict(files_data)
    uploaded_file = parameters["file"]
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    project_name = parameters["project_name"]

    virus_scan.scan_file(uploaded_file, user_email, project_name)

    success = await resources_domain.create_file(
        new_files_data, uploaded_file, project_name, user_email
    )
    if success:
        info.context.loaders.group.clear(project_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added resource files to {project_name} "
            f"project successfully",
        )
    else:
        LOGGER.error("Couldn't upload file", extra={"extra": parameters})
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to add resource files "
            f"from {project_name} project",
        )

    return SimplePayloadType(success=success)
