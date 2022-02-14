from custom_types import (
    Group,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.token import (
    get_jwt_content,
)
from newutils.vulnerabilities import (
    filter_open_vulns,
)
from typing import (
    Tuple,
)


@require_asm
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Vulnerability, ...]:
    group_name: str = parent["name"]
    user_data = await get_jwt_content(info.context)
    findings: Tuple[
        Finding, ...
    ] = await info.context.loaders.group_findings.load(group_name)
    finding_ids = [finding.id for finding in findings]
    vulns_nzr_loader = info.context.loaders.finding_vulnerabilities_nzr
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await vulns_nzr_loader.load_many_chained(finding_ids)

    return tuple(
        vulnerability
        for vulnerability in filter_open_vulns(vulnerabilities)
        if vulnerability.treatment.assigned == user_data["user_email"]
    )
