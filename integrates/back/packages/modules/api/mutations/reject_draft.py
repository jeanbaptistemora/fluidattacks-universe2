# Standard library
from typing import Any

# Third party libraries
from aioextensions import schedule
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.typing import SimplePayload as SimplePayloadType
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_finding_access,
    require_integrates,
    require_login,
)
from findings import domain as findings_domain
from mailer import findings as findings_mail
from redis_cluster.operations import redis_del_by_deps_soon


@convert_kwargs_to_snake_case
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
        if util.get_source(info.context) != 'skims':
            finding_loader = info.context.loaders.finding
            finding = await finding_loader.load(finding_id)
            schedule(
                findings_mail.send_mail_reject_draft(
                    info.context.loaders,
                    finding_id,
                    str(finding.get('title', '')),
                    str(finding.get('project_name', '')),
                    str(finding.get('analyst', '')),
                    reviewer_email
                )
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
