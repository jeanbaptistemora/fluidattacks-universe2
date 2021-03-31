# Standard library
from typing import Any

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.dal.helpers.redis import redis_del_by_deps_soon
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_finding_access,
    require_integrates,
    require_login
)
from backend.typing import SimplePayload as SimplePayloadType
from newutils import findings as finding_utils
from findings import domain as findings_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
    require_finding_access,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    finding_id: str
) -> SimplePayloadType:
    user_info = await util.get_jwt_content(info.context)
    reviewer_email = user_info['user_email']
    success = await findings_domain.reject_draft(
        info.context,
        finding_id,
        reviewer_email
    )
    if success:
        redis_del_by_deps_soon('reject_draft', finding_id=finding_id)
        finding_loader = info.context.loaders.finding
        finding = await finding_loader.load(finding_id)
        findings_domain.send_finding_mail(
            info.context.loaders,
            finding_utils.send_draft_reject_mail,
            finding_id,
            str(finding.get('title', '')),
            str(finding.get('project_name', '')),
            str(finding.get('analyst', '')),
            reviewer_email
        )
        util.cloudwatch_log(
            info.context,
            f'Security: Draft {finding_id} rejected successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to reject draft {finding_id}'
        )

    return SimplePayloadType(success=success)
