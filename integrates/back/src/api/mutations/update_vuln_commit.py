from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
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
from newutils.utils import (
    resolve_kwargs,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from vulnerabilities.domain.rebase import (
    rebase as rebase_vuln,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    vuln_commit: str,
    vuln_id: str,
    vuln_where: str,
    vuln_specific: str,
) -> SimplePayload:
    vuln_data = await info.context.loaders.vulnerability.load(vuln_id)
    finding_id: str = vuln_data["finding_id"]
    finding_data = await info.context.loaders.finding.load(finding_id)
    group_name: str = resolve_kwargs(finding_data)
    vulns_data = await info.context.loaders.finding_vulns_nzr.load(finding_id)

    success: bool = await rebase_vuln(
        finding_id=finding_id,
        finding_vulns_data=vulns_data,
        vuln_commit=vuln_commit,
        vuln_type=vuln_data["vuln_type"],
        vuln_id=vuln_id,
        vuln_where=vuln_where,
        vuln_specific=vuln_specific,
    )

    if success:
        await redis_del_by_deps(
            "update_vuln_commit",
            finding_id=finding_id,
            group_name=group_name,
        )

    return SimplePayload(success=success)
