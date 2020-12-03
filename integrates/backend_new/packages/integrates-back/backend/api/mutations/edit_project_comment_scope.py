from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from backend import util
from backend.decorators import (
    require_integrates,
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from backend.domain import project as project_domain
from backend.exceptions import PermissionDenied
from backend.typing import SimplePayload as SimplePayloadType


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    comment_id: str,
    comment_scope: str,
    project_name: str
) -> SimplePayloadType:
    success = False

    try:
        success = await project_domain.edit_comment_scope(
            comment_id,
            comment_scope,
            project_name
        )
    except PermissionDenied:
        util.cloudwatch_log(
            info.context,
            'Security: Unauthorized role attempted to edit comment scope'
        )

    return SimplePayloadType(success=success)
