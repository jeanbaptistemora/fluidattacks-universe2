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
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils.token import (
    get_jwt_content,
)
from typing import (
    Tuple,
)


@concurrent_decorators(enforce_group_level_auth_async, require_asm)
async def resolve(
    parent: Group, info: GraphQLResolveInfo, **_kwargs: None
) -> Tuple[Vulnerability, ...]:
    group_name: str = parent["name"]
    user_data = await get_jwt_content(info.context)
    findings: Tuple[
        Finding, ...
    ] = await info.context.loaders.group_findings.load(group_name)
    vulnerabilities: Tuple[
        Vulnerability, ...
    ] = await info.context.loaders.finding_vulns_nzr_typed.load_many_chained(
        finding.id for finding in findings
    )

    return tuple(
        vulnerability
        for vulnerability in vulnerabilities
        if vulnerability.treatment.assigned == user_data["user_email"]
    )
