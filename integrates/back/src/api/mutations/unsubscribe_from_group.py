from .payloads.types import (
    SimplePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
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
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str
) -> SimplePayload:
    stakeholder_info = await sessions_domain.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    await groups_domain.unsubscribe_from_group(
        loaders=loaders,
        group_name=group_name,
        email=stakeholder_email,
    )
    msg = (
        f"Security: Unsubscribed stakeholder: {stakeholder_email} "
        f"from {group_name} group successfully"
    )
    logs_utils.cloudwatch_log(info.context, msg)

    return SimplePayload(success=True)
