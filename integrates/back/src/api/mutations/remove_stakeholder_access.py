from .payloads.types import (
    RemoveStakeholderAccessPayload,
)
from .schema import (
    MUTATION,
)
from ariadne import (
    convert_kwargs_to_snake_case,
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


@MUTATION.field("removeStakeholderAccess")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    user_email: str,
    group_name: str,
) -> RemoveStakeholderAccessPayload:
    user_data = await sessions_domain.get_jwt_content(info.context)
    requester_email = user_data["user_email"]
    await groups_domain.remove_stakeholder(
        loaders=info.context.loaders,
        email_to_revoke=user_email,
        group_name=group_name,
        modified_by=requester_email,
        send_reassignment_email=True,
    )
    msg = (
        f"Security: Removed stakeholder: {user_email} from {group_name} "
        f"group successfully by {requester_email} request"
    )
    logs_utils.cloudwatch_log(info.context, msg)

    return RemoveStakeholderAccessPayload(
        success=True, removed_email=user_email
    )
