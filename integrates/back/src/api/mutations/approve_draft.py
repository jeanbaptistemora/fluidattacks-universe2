# None


from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    ApproveDraftPayload,
)
from decorators import (
    concurrent_decorators,
    delete_kwargs,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)


@convert_kwargs_to_snake_case
@delete_kwargs({"group_name"})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, draft_id: str
) -> ApproveDraftPayload:
    """Resolve approve_draft mutation."""
    user_info = await token_utils.get_jwt_content(info.context)
    reviewer_email = user_info["user_email"]
    group_name = await findings_domain.get_group(draft_id)

    success, release_date = await findings_domain.approve_draft(
        info.context, draft_id, reviewer_email
    )
    if success:
        info.context.loaders.finding.clear(draft_id)
        redis_del_by_deps_soon(
            "approve_draft",
            finding_id=draft_id,
            group_name=group_name,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Approved draft in {group_name} group successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to approve draft in {group_name} group",
        )
    return ApproveDraftPayload(release_date=release_date, success=success)
