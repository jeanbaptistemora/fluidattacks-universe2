# None


from aioextensions import (
    schedule,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from findings import (
    domain as findings_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from mailer import (
    findings as findings_mail,
)
from newutils import (
    logs as logs_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_id: str,
    justification: str,
) -> SimplePayload:
    finding_loader = info.context.loaders.finding
    finding_data = await finding_loader.load(finding_id)
    group_name = finding_data["project_name"]

    success = await findings_domain.delete_finding(
        info.context, finding_id, justification
    )
    if success:
        info.context.loaders.group_findings_all.clear(group_name)
        info.context.loaders.group_findings.clear(group_name)
        info.context.loaders.group_drafts.clear(group_name)
        info.context.loaders.finding.clear(finding_id)
        redis_del_by_deps_soon("delete_finding", finding_id=finding_id)
        justification_dict = {
            "DUPLICATED": "It is duplicated",
            "FALSE_POSITIVE": "It is a false positive",
            "NOT_REQUIRED": "Finding not required",
        }
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Deleted finding: {finding_id} successfully",
        )
        schedule(
            findings_mail.send_mail_delete_finding(
                finding_id,
                str(finding_data.get("finding", "")),
                group_name,
                str(finding_data.get("analyst", "")),
                justification_dict[justification],
            )
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to delete finding: {finding_id}",
        )

    return SimplePayload(success=success)
