from typing import Any
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from backend import (
    authz,
    util,
)
from backend.decorators import (
    require_integrates,
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from backend.domain import (
    finding as finding_domain,
    project as project_domain
)
from backend.exceptions import PermissionDenied
from backend.typing import SimplePayload as SimplePayloadType


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str
) -> SimplePayloadType:
    group_name = group_name.lower()
    user_info = await util.get_jwt_content(info.context)
    requester_email = user_info['user_email']
    success = False

    try:
        success = await project_domain.edit(
            comments="",
            group_name=group_name,
            has_drills=False,
            has_forces=False,
            has_integrates=False,
            reason="",
            requester_email=requester_email,
            subscription="continuous",
        )
    except PermissionDenied:
        util.cloudwatch_log(
            info.context,
            f'Security: Unauthorized role attempted to delete group'
        )

    if success:
        group_findings = await finding_domain.list_findings(
            [group_name], include_deleted=True
        )
        group_drafts = await finding_domain.list_drafts(
            [group_name], include_deleted=True
        )
        findings_and_drafts = (
            group_findings[0] + group_drafts[0]
        )
        await util.invalidate_cache(
            group_name,
            requester_email,
            *findings_and_drafts
        )
        await authz.revoke_cached_group_service_attributes_policies(group_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Deleted group {group_name} successfully',
        )

    return SimplePayloadType(success=success)
