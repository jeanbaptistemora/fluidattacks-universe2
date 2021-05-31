from aioextensions import schedule
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload
from db_model.findings.types import Finding
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from findings import domain as findings_domain
from mailer import findings as findings_mail
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from redis_cluster.operations import redis_del_by_deps_soon


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, finding_id: str, group_name: str
) -> SimplePayload:
    finding_loader = info.context.loaders.finding_new
    user_info = await token_utils.get_jwt_content(info.context)
    analyst_email = user_info["user_email"]
    await findings_domain.submit_draft_new(
        analyst_email, info.context, finding_id, group_name
    )
    redis_del_by_deps_soon(
        "submit_draft_new",
        finding_new_id=finding_id,
        finding_new_group=group_name,
    )
    logs_utils.cloudwatch_log(
        info.context,
        (
            f"Security: Submitted draft {finding_id} in group {group_name}"
            " successfully"
        ),
    )
    finding: Finding = await finding_loader.load((group_name, finding_id))
    schedule(
        findings_mail.send_mail_new_draft(
            info.context.loaders,
            finding.id,
            finding.title,
            finding.group_name,
            analyst_email,
        )
    )
    return SimplePayload(success=True)
