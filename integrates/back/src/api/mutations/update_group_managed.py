from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupManaged,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    turn_args_into_kwargs,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("updateGroupManaged")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
@turn_args_into_kwargs
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    comments: str,
    group_name: str,
    managed: GroupManaged,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    managed = GroupManaged(managed)
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    email = user_info["user_email"]

    await groups_domain.update_group_managed(
        loaders=loaders,
        comments=comments,
        email=email,
        group_name=group_name,
        managed=managed,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Updated managed in group {group_name} successfully",
    )

    return SimplePayload(success=True)
